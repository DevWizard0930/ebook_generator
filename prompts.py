"""
AI Prompts for eBook Generation
Each prompt is a function that returns a formatted string using the provided arguments.
"""

def book_concept_prompt():
    return """You are a professional fiction author, market researcher, and publishing strategist. Your job is to develop a unique, commercially viable standalone fiction book concept that fits within one of the three following best-selling, evergreen niches:
1. Paranormal Romance
2. Cozy Mystery
3. Self-Help (if used for nonfiction; skip this for fiction books)

Only select **Paranormal Romance** or **Cozy Mystery** for this task. Your response will be used as the foundational blueprint for a fully AI-generated book, so your concept must be both creative and structurally solid.

Follow these exact steps:

STEP 1: **Randomly select one fiction niche (Paranormal Romance OR Cozy Mystery)**
Include the niche name clearly.

STEP 2: **Select a popular, high-demand subgenre or twist within the chosen niche.**
Examples:
- Paranormal Romance: werewolf romance, vampire academy, fallen angels, fated mates
- Cozy Mystery: culinary mystery, librarian sleuth, antique shop, holiday-themed murder

STEP 3: **Generate a one-sentence commercial hook that would catch a reader's attention.**
This should be exciting, specific, and emotionally resonant.

STEP 4: **Write a detailed book concept summary (150–300 words).**
This is the full concept description that explains:
- Main character and their background
- The setting (time and place)
- The conflict or central mystery
- Key relationships (especially romantic or adversarial)
- The tone (e.g., light-hearted, spooky, romantic, emotional)
- The story's uniqueness or appeal to readers

STEP 5: **Assign a suggested word count and chapter count for the book.**
The book should be between **16,000–20,000 words**, ideally split across **10–15 chapters** depending on pacing.

Output format:
{
"niche": "Cozy Mystery",
"subgenre": "Holiday Mystery",
"hook": "A Christmas tree decorator discovers a murder weapon inside a vintage ornament box—and must solve the mystery before Christmas Eve.",
"concept_summary": "Emily, a struggling florist in a snowy Vermont town, takes on a seasonal side job decorating holiday homes. But when she opens a delivery of antique ornaments and finds a bloody letter opener tucked inside, her quiet winter gig turns into a deadly puzzle. With the help of her retired-cop father and her charming bakery rival, Emily uncovers decades-old secrets buried under tinsel and mistletoe. As the snow falls, the mystery deepens—and time runs out before the killer strikes again.",
"word_count": 17000,
"chapter_count": 13
}"""

def title_and_outline_prompt(concept):
    return f"""You are a bestselling fiction author and professional book planner. Your job is to create a compelling, structured, and emotionally engaging title and full chapter-by-chapter outline for a commercially viable standalone fiction book in either Paranormal Romance or Cozy Mystery, based on the provided concept.

Input:
Book Concept: {concept.get('concept_summary', '')}
Genre: {concept.get('niche', '')}
Subgenre: {concept.get('subgenre', '')}
Word Count Target: {concept.get('word_count', '')}
Chapter Count Target: {concept.get('chapter_count', '')}

Instructions:
STEP 1: **Create a marketable, emotionally compelling book title**
- Must fit tone and genre expectations
- Use buzzwords, emotional hooks, or theme-based phrasing
- Title must be original (not copied from existing books)

STEP 2: **Generate a full chapter-by-chapter outline**
- Use {concept.get('chapter_count', '')} to determine number of chapters
- For each chapter, include:
- Chapter number
- Chapter title (short, catchy)
- 2–5 sentence summary of what happens
- Follow fiction pacing structure:
- Chapters 1–3: Setup & conflict introduction
- Chapters 4–6: Rising tension and stakes
- Chapters 7–10: Confrontation and climax
- Final chapters: Resolution and payoff

STEP 3: **Ensure story continuity and growth**
- Character arcs should develop over time
- Escalate central conflict logically
- Resolve open threads by the final chapters

STEP 4: **Generate 5–10 genre-relevant keyword phrases**
- These keywords help with search visibility and marketing
- Use multi-word phrases (not single terms)
- Include emotional, setting-based, or theme-based phrases
- Format output as a comma-separated list

Output Format (JSON):
{{
"title": "Whispers Beneath the Willow",
"chapters": [
{{
"chapter_number": 1,
"chapter_title": "The Delivery",
"summary": "Emily receives a mysterious box of antique Christmas ornaments, one of which contains a bloody letter opener. Her curiosity piqued, she begins asking around town."
}},
{{
"chapter_number": 2,
"chapter_title": "Tinsel and Tension",
"summary": "A visit to the antique shop reveals the ornaments were part of an estate sale from a woman who disappeared in the 80s. Emily senses this job may be more than festive cheer."
}}
// ...additional chapters
],
"keywords": [
"cozy Christmas mystery",
"small town secrets",
"paranormal holiday romance",
"antique shop mystery",
"missing person cold case",
"female amateur sleuth",
"holiday suspense with heart",
"second chance healing romance"
]
}}"""

def chapter_generation_prompt(book_title, genre, chapter_number, chapter_title, chapter_summary, previous_chapters):
    return f"""You are a professional book author. Your task is to write a complete chapter of a standalone commercial book based on the provided outline and genre. The chapter must reflect the book's tone, style, and structure — whether it is fiction or nonfiction.

Input:
Book Title: {book_title}
Genre: {genre}
Style: Fiction
Chapter Number: {chapter_number}
Chapter Title: {chapter_title}
Chapter Summary: {chapter_summary}
Previous Chapter Summaries (optional):
{previous_chapters}

Instructions:
- Write the full chapter based on the chapter summary
- Match the tone, voice, and structure appropriate to the genre and style
- For fiction:
- Focus on character development, conflict, emotional tone, and story momentum
- Maintain consistency if previous chapters are included
- Use professional grammar, punctuation, and formatting
- Do NOT include: chapter number, chapter title, summaries, or notes only the chapter text
- Target Word Count: 900–1,200 words

Output Format:
Return only the full chapter in plain story or instructional text. No markdown, titles, or commentary."""

def back_cover_blurb_prompt(book_title, genre, concept_summary):
    return f"""You are a professional copywriter and bestselling book blurb specialist. Your task is to write a short, emotionally engaging, and commercially appealing back cover blurb for a standalone book in the specified genre.

Input:
Book Title: {book_title}
Genre: {genre}
Style: Fiction
Book Summary or Outline: {concept_summary}

Instructions:
- Length: 150–250 words
- Style:
- For fiction: Focus on character, conflict, stakes, setting, and intrigue
- Tone must match the genre (e.g., emotional for romance, witty for cozy mystery, inspiring for self-help)
- Make the reader curious without spoiling the entire book
- Use strong openers, short impactful sentences, and persuasive phrasing
- Do NOT use quotes, reviews, or bullet points — just a professional back cover blurb

Output Format:
Return a single paragraph (or two short paragraphs) of plain text only."""

def cover_image_prompt(book_title, genre):
    return f"""You are a creative prompt engineer for AI image generators.

Your task is to generate a vivid and creative **text-only prompt** that describes a fictional, cozy scene suitable for a vertical book cover image.

Input:
Book Title: {book_title}
Genre: {genre}
Style: Fiction
Tone/Mood: cozy

Instructions:
- Format: Portrait / Vertical orientation
- Resolution: 1024 x 1792 pixels
- Style: Clean, high-quality, realistic or semi-illustrative art
- Genre-specific visual tone:
- Paranormal Romance: dreamlike, moody, mystical elements
- Cozy Mystery: warm, small-town, charming, vintage or cartoonish details
- Do NOT include any real text — this image will be used as a base only
- Do NOT include faces or specific celebrities
- Avoid clutter — prioritize clarity and genre alignment

Output Format:
A single, clean image prompt ready for DALL-E 3."""

# def cover_image_prompt(book_title, genre):
#     return f"""You are an AI image generation assistant. Your task is to generate a **vertical book cover image** in the correct aspect ratio (1024x1792 pixels) based on the book's genre, mood, and visual tone.

# Input:
# Book Title: {book_title}
# Genre: {genre}
# Style: Fiction
# Tone/Mood: cozy

# Instructions:
# - Format: Portrait / Vertical orientation
# - Resolution: 1024 x 1792 pixels
# - Style: Clean, high-quality, realistic or semi-illustrative art
# - Genre-specific visual tone:
# - Paranormal Romance: dreamlike, moody, mystical elements
# - Cozy Mystery: warm, small-town, charming, vintage or cartoonish details
# - Do NOT include any real text — this image will be used as a base only
# - Do NOT include faces or specific celebrities
# - Avoid clutter — prioritize clarity and genre alignment

# Output Format:
# A single, clean image prompt ready for DALL-E 3."""

def streetlib_metadata_prompt(book_data, Config):
    return f"""You are a professional digital publishing assistant, expert in StreetLib's ebook publishing requirements. Based on the book's details below, generate all metadata fields exactly as needed for StreetLib's HUB form.

Input:
Book Title: {book_data.get('title', '')}
Subtitle (optional): {book_data.get('subtitle', '')}
Series Title & Number (optional): {book_data.get('series', '')}
Author Name (Surname, Firstname): {Config.AUTHOR_NAME}
Co‑Authors/Contributors (if any, with roles): {book_data.get('contributors', '')}
Publication Year: {Config.PUBLICATION_YEAR}
Language: {Config.LANGUAGE}
Short Synopsis: {book_data.get('synopsis', '')}
Keywords (leave blank—generate below)
Genre/Subgenre: {book_data.get('genre', '')}
Estimated Word Count: {book_data.get('word_count', '')}
Target Age Range (e.g. Adult, Young Adult, 18+ if adult content): {Config.AGE_RATING}
User Rights (e.g. "I am the author and copyright owner")
Public Domain (Yes/No): No
Adult Content (Yes/No): No

Instructions:
1. Short Description:
Up to 4,000 characters, without title or formatting.
Should engage readers, avoid discounts/offers, follow StreetLib's "Synopsis" field guidance.

2. Keywords:
Provide exactly 7 comma‑separated keyword phrases.
Use reader‑friendly, specific search terms aligned with genre and concept.
Follow best practices (e.g. "cozy small‑town mystery" not "mystery").

3. BISAC Categories:
Provide 1–3 BISAC categories with correct name and code.
At least 1 required.
Choose most specific subgenre.
Use latest 2024 edition standards.

4. Language & Age Range:
Confirm language code.
Set age range (e.g., "Adult" or "18+" only if adult content).

5. Cover Upload Info:
Outer cover specs: JPG/PNG RGB, ~1875 × 2500 px.
Must match title/author exactly as entered.
No spine or text price info.

6. Publication Details:
Suggested price in USD and EUR.
Publication year.
User rights, Public Domain, Adult content flags.

Output Format (JSON):
{{
"title": "...",
"subtitle": "...",
"series": {{ "name": "...", "number": 1 }},
"author": "Surname, Firstname",
"contributors": [ {{ "name": "X Y", "role": "Illustrator" }} ],
"publication_year": 2025,
"language": "English",
"age_rating": "Adult",
"synopsis": "...", // <4 000 chars
"keywords": "mystery cottage crime, cozy small-town mystery, amateur sleuth... (7 total)",
"bisac_categories": [
{{ "name": "FICTION / Mystery & Detective / Cozy", "code": "FIC022130" }},
{{ "name": "FICTION / Family Life / General", "code": "FIC027030" }}
],
"thema_category": "…optional…",
"cover_specs": {{
"outer": "JPG 1875×2500px RGB, no price/text/spine",
"inner": "will be auto-generated"
}},
"suggested_price_usd": 2.99,
"suggested_price_eur": 2.49,
"user_rights": "I am the author and copyright owner",
"public_domain": "No",
"adult_content": "No"
}}""" 