import asyncio
from Luci import create_master_prompt

async def main():
    model_name = "cerina" 
    # Define your list of prompts
    prompts = [
        "Generate the recends progress of revmaxx llc",
        "Explain the benefits of using AI in healthcare."
    ]

    # Generate master prompt using the standalone function
    master_prompt = await create_master_prompt(
        model_name=model_name,
        prompts=prompts,
        connected=True,  # Set to True to enable passing info between prompts
        search=True  # Set to True to enable search functionality
    )

    print("Generated Master Prompt:", master_prompt)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
