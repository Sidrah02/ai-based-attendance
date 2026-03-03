"""
Initialize the database with sample data.

This script creates:
1. All database tables (via SQLAlchemy)
2. Sample admin account
3. Sample subjects

Run with: python scripts/init_db.py
"""

import asyncio
from app.config.database import connect_db, AsyncSessionLocal
from app.models.admin import Admin
from app.models.subject import Subject


async def init_db():
    """Initialize database with tables and sample data."""
    
    print("🔄 Connecting to database...")
    await connect_db()
    print("✅ Database connected and tables created.")
    
    async with AsyncSessionLocal() as session:
        try:
            # Check if admin already exists
            existing_admin = await session.query(Admin).filter(
                Admin.email == "admin@attendance.com"
            ).first()
            
            if not existing_admin:
                print("\n📝 Creating sample admin account...")
                admin = Admin(
                    name="System Administrator",
                    email="admin@attendance.com",
                    password=Admin.hash_password("admin123"),
                    role="admin"
                )
                session.add(admin)
                await session.commit()
                print(f"✅ Admin created: {admin.email}")
            else:
                print("⏭️  Admin already exists, skipping...")
            
            # Check if subjects already exist
            existing_subjects = await session.query(Subject).count()
            
            if existing_subjects == 0:
                print("\n📝 Creating sample subjects...")
                subjects = [
                    Subject(
                        subject_name="Introduction to Python",
                        faculty_name="Dr. John Smith",
                        semester="Spring 2026"
                    ),
                    Subject(
                        subject_name="Data Structures",
                        faculty_name="Prof. Jane Doe",
                        semester="Spring 2026"
                    ),
                    Subject(
                        subject_name="Web Development",
                        faculty_name="Dr. Mike Johnson",
                        semester="Spring 2026"
                    ),
                    Subject(
                        subject_name="Database Systems",
                        faculty_name="Prof. Sarah Williams",
                        semester="Spring 2026"
                    ),
                ]
                session.add_all(subjects)
                await session.commit()
                print(f"✅ Created {len(subjects)} sample subjects")
            else:
                print(f"⏭️  Subjects already exist ({existing_subjects} found), skipping...")
            
            print("\n✨ Database initialization complete!")
            print("\n📋 Sample Admin Credentials:")
            print("   Email: admin@attendance.com")
            print("   Password: admin123")
            print("\n⚠️  Change these credentials in production!")
            
        except Exception as e:
            print(f"❌ Error during initialization: {e}")
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(init_db())
