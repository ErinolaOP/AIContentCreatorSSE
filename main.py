from app.agents.script_writer import generate_script


def main():

    topic = "Hidden AI websites"

    script = generate_script(topic)

    print("\nGenerated Script:\n")
    print(script)


if __name__ == "__main__":
    main()