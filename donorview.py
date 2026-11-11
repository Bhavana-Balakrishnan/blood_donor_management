
from mysql import connector
from datetime import datetime


class BloodDonorManager:

    def __init__(self):
        self.connection = connector.connect(
            user="root",
            password="Bhavana@123",
            host="localhost",
            database="blood_db_aug26"
        )
        print("Connected successfully")

    # GET SINGLE DONOR
    def get_object(self, id=None):
        try:
            cursor = self.connection.cursor()

            query = "SELECT * FROM donor WHERE id=%s"
            values = (id,)

            cursor.execute(query, values)
            record = cursor.fetchone()

            return record

        except Exception as e:
            print("Error:", e)
            return None

    # INSERT DONOR
    def post(self, **kwargs):
        try:
            cursor = self.connection.cursor()

            columns = ["name", "blood_group", "phone", "city", "last_donation"]

            values = tuple(kwargs[column] for column in columns)

            query = """
                INSERT INTO donor
                (name, blood_group, phone, city, last_donation)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, values)
            self.connection.commit()

            print("Data inserted successfully!")

            return True

        except Exception as e:
            print("Error:", e)
            self.connection.rollback()
            return False

    # GET ALL DONORS
    def get(self):
        try:
            cursor = self.connection.cursor()

            query = "SELECT * FROM donor"

            cursor.execute(query)
            records = cursor.fetchall()

            return records

        except Exception as e:
            print("Error:", e)
            return []

    # RETRIEVE DONOR BY ID
    def retrieve(self, id=None):
        try:
            record = self.get_object(id=id)

            if record is not None:
                print(record)
                return record
            else:
                print("No donor found")
                return None

        except Exception as e:
            print("Error:", e)
            return None

    # DELETE DONOR
    def delete(self, id=None):
        try:
            record = self.get_object(id=id)

            if record is not None:
                cursor = self.connection.cursor()

                query = "DELETE FROM donor WHERE id=%s"

                cursor.execute(query, (id,))
                self.connection.commit()

                print("Donor deleted successfully!")

                return True

            else:
                print("No donors found")
                return False

        except Exception as e:
            print("Error:", e)
            self.connection.rollback()
            return False

    # UPDATE DONOR
    def put(self, id=None, **kwargs):
        try:
            record = self.get_object(id=id)

            if record is not None:

                allowed_columns = [
                    "name",
                    "blood_group",
                    "phone",
                    "city",
                    "last_donation"
                ]

                if not kwargs:
                    return False, "No fields provided for update"

                for key in kwargs:
                    if key not in allowed_columns:
                        return False, f"Invalid column: {key}"

                cursor = self.connection.cursor()

                placeholder = ", ".join(
                    f"{key}=%s" for key in kwargs.keys()
                )

                query = f"UPDATE donor SET {placeholder} WHERE id=%s"

                values = list(kwargs.values())
                values.append(id)

                cursor.execute(query, values)
                self.connection.commit()

                return True, "Donor updated successfully"

            else:
                return False, "No donors found"

        except Exception as e:
            print("Error:", e)
            self.connection.rollback()
            return False, str(e)

    # CLOSE DATABASE CONNECTION
    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")


# MAIN PROGRAM
if __name__ == "__main__":

    donor_instance = BloodDonorManager()

    # Display all donors
    print(donor_instance.get())

    # Retrieve donor
    # donor_instance.retrieve(id=1)

    # Insert donor
    # donor_instance.post(
    #     name="rahul",
    #     blood_group="O+",
    #     phone="9878989898",
    #     city="kochi",
    #     last_donation=datetime.today()
    # )

    # Update donor
    # status, message = donor_instance.put(
    #     id=1,
    #     name="rahul",
    #     blood_group="O+",
    #     phone="1234567890",
    #     city="kochi",
    #     last_donation=datetime.today()
    # )
    # print(status, message)

    # Delete donor
    # donor_instance.delete(id=4)

    donor_instance.close()
