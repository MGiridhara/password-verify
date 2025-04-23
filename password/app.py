from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

# Function to perform brute force attack using a wordlist
def brute_force_crack(hash_value, wordlist_path):
    try:
        with open(wordlist_path, 'r', encoding='utf-8') as file:
            for word in file:
                word = word.strip()
                hashed_word = hashlib.md5(word.encode()).hexdigest()
                if hashed_word == hash_value:
                    return word  # Password found
    except FileNotFoundError:
        return "Wordlist file not found."
    return None  # Password not found

@app.route("/", methods=["GET", "POST"])
def index():
    cracked_password = None
    message = None
    
    if request.method == "POST":
        password = request.form.get("password")
        wordlist = "wordlist.txt"  # Wordlist file containing possible passwords
        
        # Hash the input password
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        # Try to crack it
        cracked_password = brute_force_crack(password_hash, wordlist)
        
        if cracked_password is None:
            message = "Password not found in the wordlist."
        elif cracked_password == "Wordlist file not found.":
            message = "Error: Wordlist file is missing."
    
    return render_template("index.html", cracked_password=cracked_password, message=message)

if __name__ == "__main__":
    app.run(debug=True)
