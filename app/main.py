# app/main.py

from fastapi import FastAPI
from app.database.mysql import engine, Base
from app.models import user, role, driver, trip, payment, feedback, subscription, referral 
from app.routes import (
    user, driver, role, trip,
    payment, feedback, subscription, referral, trip_log, search_data, live_trip, formality
)  # you'll create this next
from app.routes import driver as driver_router
from app.routes import uploads
from app.routes import favorite_driver as favorite_router


app = FastAPI()

# Create MySQL tables
Base.metadata.create_all(bind=engine)

# Add your routes
app.include_router(user.router, prefix="/users", tags=["Users"])
# app.include_router(driver.router, prefix="/drivers", tags=["Drivers"])
app.include_router(driver_router.router)
app.include_router(uploads.router)
app.include_router(formality.router, prefix="/formalities", tags=["Formalities"])
app.include_router(role.router, prefix="/roles", tags=["Roles"])
app.include_router(search_data.router, prefix="/search", tags=["Search History"])
app.include_router(trip.router, prefix="/trips", tags=["Trips"])
app.include_router(live_trip.router, prefix="/live-trip", tags=["Live Trip"])
app.include_router(trip_log.router, prefix="/trip-logs", tags=["Trip Logs"])
app.include_router(subscription.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(referral.router, prefix="/referrals", tags=["Referrals"])
app.include_router(favorite_router.router)
app.include_router(feedback.router, prefix="/feedbacks", tags=["Feedbacks"])
app.include_router(payment.router, prefix="/payments", tags=["Payments"])
