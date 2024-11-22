class User(Base):
    # ... existing code ...
    password = Column(String(255), nullable=False)  # Added length

class Contact(Base):
    # No changes needed - all String columns have lengths

class Enroll(Base, TimestampMixin):
    # ... existing code ...
    membershipPlan = Column(String(100), nullable=False)  # Reduced from 300 to more reasonable length
    # Other fields are fine

class Trainer(Base):
    # No changes needed - all String columns have lengths

class MembershipPlan(Base):
    # No changes needed - all String columns have lengths

class Gallery(Base, TimestampMixin):
    # No changes needed - all String columns have lengths

class Attendance(Base):
    # ... existing code ...
    selectDate = Column(DateTime, default=datetime.now(datetime.UTC), nullable=False)  # Fixed deprecated datetime
    # Other fields are fine