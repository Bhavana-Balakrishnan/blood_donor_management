
import streamlit as st
from donorview import BloodDonorManager
from datetime import date

st.set_page_config(page_title="Blood Donor Management", layout="wide")

donor_instance = BloodDonorManager()

blood_groups = ["A+", "A-", "O+", "O-", "B+", "B-"]

tab1, tab2, tab3, tab4 = st.tabs([
    "Add Donor",
    "View Donors",
    "Update Details",
    "Delete Donor"
])


# ---------------- TAB 1: ADD DONOR ----------------

with tab1:

    st.header("Add New Donor")

    name = st.text_input("Enter donor name")
    phone = st.text_input("Enter phone number")
    blood_group = st.selectbox(
        "Select blood group",
        blood_groups,
        key="add_blood_group"
    )
    city = st.text_input("Enter your city")
    last_donation = st.date_input(
        "Enter last donation date",
        value=date.today()
    )

    if st.button("Submit", key="add_submit"):

        if name and phone and city:

            status = donor_instance.post(
                name=name,
                blood_group=blood_group,
                phone=phone,
                city=city,
                last_donation=last_donation
            )

            if status:
                st.success("Donor added successfully!")
            else:
                st.error("Unable to add donor. Please check the error.")

        else:
            st.warning("Please fill all the fields.")


# ---------------- TAB 2: VIEW DONORS ----------------

with tab2:

    st.title("View Blood Donor Details")

    records = donor_instance.get()

    if records:
        st.table(records)
    else:
        st.warning("No donors found.")


# ---------------- TAB 3: UPDATE DONOR ----------------

with tab3:

    st.title("Update Donor Details")

    records = donor_instance.get()

    if records:

        donor_ids = [r[0] for r in records]
        donor_id = st.selectbox(
            "Select donor ID",
            donor_ids,
            key="update_id"
        )

        record = donor_instance.get_object(id=donor_id)

        if record:

            name = st.text_input(
                "Enter donor name",
                value=record[1],
                key="update_name"
            )

            blood_group_selected = st.selectbox(
                "Select blood group",
                blood_groups,
                index=(
                    blood_groups.index(str(record[2]).strip())
                    if str(record[2]).strip() in blood_groups
                    else 0
                ),
                key="update_blood_group"
            )

            phone = st.text_input(
                "Enter donor phone number",
                value=str(record[3]),
                key="update_phone"
            )

            city = st.text_input(
                "Enter your city",
                value=record[4],
                key="update_city"
            )

            donation_date = record[5]

            if isinstance(donation_date, date):
                default_date = donation_date
            else:
                default_date = date.today()

            last_donation = st.date_input(
                "Last donation date",
                value=default_date,
                key="update_date"
            )

            if st.button("Update", key="update_submit"):

                status, message = donor_instance.put(
                    id=donor_id,
                    name=name,
                    blood_group=blood_group_selected,
                    phone=phone,
                    city=city,
                    last_donation=last_donation
                )

                if status:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    else:
        st.warning("No donors found.")


# ---------------- TAB 4: DELETE DONOR ----------------

with tab4:

    st.title("Delete Donor Details")

    records = donor_instance.get()

    if records:

        donor_ids = [r[0] for r in records]

        delete_id = st.selectbox(
            "Select donor ID to delete",
            donor_ids,
            key="delete_id"
        )

        if st.button("Delete Donor", key="delete_submit"):

            status = donor_instance.delete(id=delete_id)

            if status:
                st.success("Donor deleted successfully!")
                st.rerun()
            else:
                st.error("Unable to delete donor.")

    else:
        st.warning("No donors found.")
