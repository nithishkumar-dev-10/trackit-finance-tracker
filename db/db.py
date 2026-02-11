import os
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



# =========================
# DATABASE CONNECTION
# =========================
def connectdb():
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise Exception("DATABASE_URL is not set")

    return psycopg2.connect(DATABASE_URL)


# =========================
# AUTH
# =========================
def register(username, password):
    con = cursor = None
    try:
        con = connectdb()
        cursor = con.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username = %s",
            (username,)
        )
        if cursor.fetchone():
            return False, "Username already exists"

        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        con.commit()
        return True, "User registered successfully"

    except Exception as err:
        return False, f"Database error: {err}"

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def login(username, password):
    con = cursor = None
    try:
        con = connectdb()
        cursor = con.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            return user["id"]

        return None

    except Exception:
        return None

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


# =========================
# INCOME
# =========================
def add_income(user_id, amount, source, date):
    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be greater than zero"

        date = datetime.strptime(date, "%Y-%m-%d").date()

        con = connectdb()
        cursor = con.cursor()

        cursor.execute(
            "INSERT INTO income (user_id, date, amount, source) VALUES (%s, %s, %s, %s)",
            (user_id, date, amount, source)
        )
        con.commit()
        return True, "Income added successfully"

    except Exception as err:
        return False, f"Database error: {err}"

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def income_details(user_id):
    con = cursor = None
    try:
        con = connectdb()
        cursor = con.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            "SELECT id, date, amount, source FROM income WHERE user_id = %s ORDER BY date DESC",
            (user_id,)
        )
        return True, cursor.fetchall()

    except Exception as err:
        return False, f"Database error: {err}"

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def delete_income(user_id, income_id):
    con = cursor = None
    try:
        con = connectdb()
        cursor = con.cursor()

        cursor.execute(
            "DELETE FROM income WHERE id = %s AND user_id = %s",
            (income_id, user_id)
        )
        con.commit()

        return (True, "Income deleted successfully") if cursor.rowcount else (False, "Not authorized")

    except Exception as err:
        return False, f"Database error: {err}"

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


# =========================
# EXPENSE
# =========================
def add_expense(user_id, amount, date, purpose):
    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be greater than zero"

        date = datetime.strptime(date, "%Y-%m-%d").date()

        con = connectdb()
        cursor = con.cursor()

        cursor.execute(
            "INSERT INTO expense (user_id, date, amount, purpose) VALUES (%s, %s, %s, %s)",
            (user_id, date, amount, purpose)
        )
        con.commit()
        return True, "Expense added successfully"

    except Exception as err:
        return False, f"Database error: {err}"

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def expense_details(user_id):
    con = cursor = None
    try:
        con = connectdb()
        cursor = con.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            "SELECT id, date, amount, purpose FROM expense WHERE user_id = %s ORDER BY date DESC",
            (user_id,)
        )
        return True, cursor.fetchall()

    except Exception as err:
        return False, f"Database error: {err}"

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def delete_expense(user_id, expense_id):
    con = cursor = None
    try:
        con = connectdb()
        cursor = con.cursor()

        cursor.execute(
            "DELETE FROM expense WHERE id = %s AND user_id = %s",
            (expense_id, user_id)
        )
        con.commit()

        return (True, "Expense deleted successfully") if cursor.rowcount else (False, "Not authorized")

    except Exception as err:
        return False, f"Database error: {err}"

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


# =========================
# SUMMARY
# =========================
def balance(user_id):
    con = cursor = None
    try:
        con = connectdb()
        cursor = con.cursor()

        cursor.execute(
            "SELECT COALESCE(SUM(amount),0) FROM income WHERE user_id = %s",
            (user_id,)
        )
        total_income = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COALESCE(SUM(amount),0) FROM expense WHERE user_id = %s",
            (user_id,)
        )
        total_expense = cursor.fetchone()[0]

        return True, {
            "balance": total_income - total_expense,
            "total_income": total_income,
            "total_expense": total_expense
        }

    except Exception as err:
        return False, f"Database error: {err}"

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def monthly_summary(user_id, year, month):
    con = cursor = None
    try:
        year, month = int(year), int(month)

        con = connectdb()
        cursor = con.cursor()

        cursor.execute(
            """
            SELECT COALESCE(SUM(amount),0)
            FROM income
            WHERE user_id=%s
            AND EXTRACT(YEAR FROM date)=%s
            AND EXTRACT(MONTH FROM date)=%s
            """,
            (user_id, year, month)
        )
        income = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COALESCE(SUM(amount),0)
            FROM expense
            WHERE user_id=%s
            AND EXTRACT(YEAR FROM date)=%s
            AND EXTRACT(MONTH FROM date)=%s
            """,
            (user_id, year, month)
        )
        expense = cursor.fetchone()[0]

        return True, {
            "monthly_income": income,
            "monthly_expense": expense,
            "monthly_balance": income - expense
        }

    except Exception as err:
        return False, f"Error: {err}"

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


# =========================
# PROFILE
# =========================
def get_user_by_id(user_id):
    con = cursor = None
    try:
        con = connectdb()
        cursor = con.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            "SELECT id, username FROM users WHERE id = %s",
            (user_id,)
        )
        return cursor.fetchone()

    except Exception:
        return None

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def change_password(user_id, old_password, new_password):
    con = cursor = None
    try:
        con = connectdb()
        cursor = con.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            "SELECT password FROM users WHERE id = %s",
            (user_id,)
        )
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password"], old_password):
            return False, "Old password is incorrect"

        new_hashed = generate_password_hash(new_password)

        cursor = con.cursor()
        cursor.execute(
            "UPDATE users SET password = %s WHERE id = %s",
            (new_hashed, user_id)
        )
        con.commit()

        return True, "Password updated successfully"

    except Exception as err:
        return False, f"Database error: {err}"

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def init_db():
    con = cursor = None
    try:
        con = connectdb()
        cursor = con.cursor()

        # USERS TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(150) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """)

        # INCOME TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            date DATE NOT NULL,
            amount FLOAT NOT NULL,
            source VARCHAR(255)
        );
        """)

        # EXPENSE TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS expense (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            date DATE NOT NULL,
            amount FLOAT NOT NULL,
            purpose VARCHAR(255)
        );
        """)

        con.commit()

    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()