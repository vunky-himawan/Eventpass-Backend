from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from infrastructure.database.models.event import EventModel
from infrastructure.database.models.speaker import SpeakerModel
from infrastructure.database.models.event_speaker import EventSpeakerModel

async def event_speaker_seeder(db: AsyncSession):
    try:
        query = select(EventModel)
        result = await db.execute(query)
        events = result.scalars().all()

        speakers = {
            "Tech Summit 2023: Innovating the Future": [
                {
                    "name": "Dr. Sophia Alvarez",
                    "title": "AI Researcher & Innovator",
                    "social_media_links": "https://linkedin.com/in/sophiaalvarez",
                    "company": "FutureTech Labs"
                },
                {
                    "name": "Michael Zhang",
                    "title": "CTO & Tech Visionary",
                    "social_media_links": "https://linkedin.com/in/michaelzhang",
                    "company": "InnovateX Inc."
                }
            ],
            "Culinary Artistry: The Fusion of Flavors": [
                {
                    "name": "Chef Emma Laurent",
                    "title": "Michelin Star Chef",
                    "social_media_links": "https://linkedin.com/in/chefemma",
                    "company": "La Cuisine Fine Dining"
                },
                {
                    "name": "Luca Moretti",
                    "title": "Culinary Artist & Food Blogger",
                    "social_media_links": "https://linkedin.com/in/lucacooks",
                    "company": "Taste the World"
                }
            ],
            "Mind & Motion: Yoga and Wellness Retreat": [
                {
                    "name": "Aarav Patel",
                    "title": "Yoga Master & Wellness Coach",
                    "social_media_links": "https://linkedin.com/in/aaravpatel",
                    "company": "SoulFlow Yoga"
                },
                {
                    "name": "Elena Rivera",
                    "title": "Mindfulness Expert",
                    "social_media_links": "https://linkedin.com/in/elenarivera",
                    "company": "Mindful Balance Co."
                }
            ],
            "Future Builders: Coding for Tomorrow": [
                {
                    "name": "James Carter",
                    "title": "Full-Stack Developer & Educator",
                    "social_media_links": "https://linkedin.com/in/jamescarter",
                    "company": "CodeCraft Academy"
                },
                {
                    "name": "Li Wei",
                    "title": "Tech Lead & Open Source Advocate",
                    "social_media_links": "https://linkedin.com/in/liwei",
                    "company": "Open Source Futures"
                }
            ],
            "EcoWorld: Sustainability and Innovation Expo": [
                {
                    "name": "Dr. Olivia Thompson",
                    "title": "Environmental Scientist",
                    "social_media_links": "https://linkedin.com/in/oliviathompson",
                    "company": "Green Innovators"
                },
                {
                    "name": "Ethan Williams",
                    "title": "Sustainability Consultant",
                    "social_media_links": "https://linkedin.com/in/ethanwilliams",
                    "company": "Sustainable Futures Ltd."
                }
            ],
            "Artistry Unleashed: A Creative Experience": [
                {
                    "name": "Sophia Hart",
                    "title": "Visual Artist & Illustrator",
                    "social_media_links": "https://linkedin.com/in/sophiahart",
                    "company": "Hart Studio"
                },
                {
                    "name": "Noah Kim",
                    "title": "Digital Art Specialist",
                    "social_media_links": "https://linkedin.com/in/noahkim",
                    "company": "Pixel Perfect Creations"
                }
            ]
        }


        for event in events:

            for i, speaker in enumerate(speakers[event.title]):
                new_speaker = SpeakerModel(
                    name=speaker["name"],
                    title=speaker["title"],
                    social_media_links=speaker["social_media_links"],
                    company=speaker["company"],
                )

                db.add(new_speaker)
                await db.flush()

                new_event_speaker = EventSpeakerModel(
                    event_id=event.event_id,
                    speaker_id=new_speaker.speaker_id
                )

                db.add(new_event_speaker)
                await db.flush()


        await db.commit()
        await db.refresh(new_speaker)
        await db.refresh(new_event_speaker)

    except Exception as e:
        await db.rollback()
        print(f"Error seeding event speakers: {e}")