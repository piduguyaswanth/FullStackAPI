from flask import Flask, request, jsonify

app = Flask(__name__)

# User details
FULL_NAME = "yashwanthpidugu"       # lowercase
DOB = "25052005"                    # ddmmyyyy
EMAIL = "yashwanthpidugu678@gmail.com"
ROLL_NUMBER = "22BCE8695"


def alternating_caps(s: str) -> str:
    """Convert string into alternating uppercase/lowercase pattern."""
    return "".join(ch.upper() if i % 2 == 0 else ch.lower() for i, ch in enumerate(s))


@app.route("/", methods=["GET"])
def home():
    """Health check endpoint."""
    return jsonify({"message": "Server is running ✅"}), 200


@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        # Validate request JSON
        if not request.is_json:
            return jsonify({"is_success": False, "error": "Invalid JSON format"}), 400

        req_data = request.get_json()
        data = req_data.get("data", [])

        if not isinstance(data, list):
            return jsonify({"is_success": False, "error": "'data' must be a list"}), 400

        # Containers
        odd_numbers, even_numbers, alphabets, specials = [], [], [], []
        total_sum = 0
        concat_alpha_original = ""  # Keep original case for concat_string

        for item in data:
            if isinstance(item, str):
                if item.isdigit():  # Numbers
                    num = int(item)
                    (even_numbers if num % 2 == 0 else odd_numbers).append(item)
                    total_sum += num
                elif item.isalpha():  # Alphabets
                    alphabets.append(item.upper())  # Uppercase in array
                    concat_alpha_original += item  # Original case for concat_string
                else:  # Special characters
                    specials.append(item)
            else:
                specials.append(str(item))  # Convert non-string to string special char

        # Prepare concatenated string
        reversed_alpha = concat_alpha_original[::-1]
        concat_string = alternating_caps(reversed_alpha)

        # Build response in required order
        response = {
            "is_success": True,
            "user_id": f"{FULL_NAME}_{DOB}",
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": specials,
            "sum": str(total_sum),
            "concat_string": concat_string,
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"is_success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
