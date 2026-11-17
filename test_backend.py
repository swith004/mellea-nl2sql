import mellea

def main():
    session = mellea.start_session(
        backend_name="ollama",
        model_id="granite4.1:3b"
    )

    response = session.instruct(
        "Explain what a relational database is in one sentence."
    )

    print(response)

if __name__ == "__main__":
    main()
    