import pyodbc

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=ERP;"
    "UID=sa;"
    "PWD=Abc@123;"
)

def get_connection():
    """Tạo và trả về kết nối đến SQL Server"""
    return pyodbc.connect(CONNECTION_STRING)

# --- Thêm hàm lấy dữ liệu bảng UserFavourite ---
def get_all_user_favourites():
    """Lấy tất cả bản ghi trong bảng UserFavourite, trả về list[dict]"""
    query = """
    SELECT id, userID, itemID, itemType, rating FROM UserFavourite
    """
    result = []
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))
    return result

# --- Các hàm khác giữ nguyên ---
def test_connection():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT GETDATE()")
            row = cursor.fetchone()
            print("Kết nối thành công, thời gian hiện tại:", row[0])
    except Exception as e:
        print("Kết nối thất bại!", e)

# test_connection()
