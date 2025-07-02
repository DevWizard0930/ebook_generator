from ai_generator import AIGenerator
from prompts import cover_image_prompt

def main():
    ai = AIGenerator()
    prompt = ai.generate_cover_image_prompt("Moonlit Whispers: A Werewolf's Healing Love", "Paranormal Romance")
    output_path = "output/test_cover.png"
    try:
        result = ai.generate_cover_image(prompt, output_path)
        print(f"Cover image generated at: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()