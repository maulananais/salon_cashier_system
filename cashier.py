import os
from db import cursor, db
from prettytable import PrettyTable

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fungsi untuk menampilkan database transaksi
def cashier_show_database():
    clear_screen()
    print("\nDaftar Transaksi:")
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    
    if rows:
        table = PrettyTable()
        table.field_names = ["ID", "Nama", "Tipe", "Layanan", "Biaya Layanan", "Biaya VIP", "PPN", "Total", "Booking", "Tanggal"]
        for row in rows:
            table.add_row([
                row[0],
                row[1],
                row[7],  # customer_type
                row[2],
                f"Rp {row[3]:,.2f}",
                f"Rp {row[8]:,.2f}",  # vip_fee
                f"Rp {row[4]:,.2f}",
                f"Rp {row[5]:,.2f}",
                'Ya' if row[6] else 'Tidak',
                row[9]  # Assuming the date is now in the 10th column
            ])
        print(table)
        print("\n")
    else:
        print("Tidak ada transaksi yang tersedia.\n")

# Fungsi untuk menghapus transaksi berdasarkan ID
def delete_transaction():
    clear_screen()
    cashier_show_database()  # Tampilkan daftar transaksi agar kasir bisa melihat ID transaksi

    try:
        transaction_id = int(input("Masukkan ID transaksi yang ingin dihapus: "))
        clear_screen()
        
        # Periksa apakah transaksi ada dalam database
        cursor.execute("SELECT * FROM transactions WHERE id = %s", (transaction_id,))
        transaction = cursor.fetchone()

        if transaction:
            confirm = input(f"Apakah Anda yakin ingin menghapus transaksi dengan ID {transaction_id}? (y/n): ")
            clear_screen()
            if confirm.lower() == 'y':
                cursor.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))
                db.commit()
                print(f"Transaksi dengan ID {transaction_id} berhasil dihapus.\n")
            else:
                print("Penghapusan dibatalkan.\n")
        else:
            print(f"Transaksi dengan ID {transaction_id} tidak ditemukan.\n")
    except ValueError:
        print("ID yang dimasukkan tidak valid. Harap masukkan angka yang sesuai.\n")

# Fungsi untuk menampilkan laporan pendapatan
def show_income_report():
    clear_screen()
    print("\nLaporan Pendapatan:")
    cursor.execute("SELECT SUM(total_price) FROM transactions")
    total_income = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(service_price) FROM transactions")
    total_service = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(vip_fee) FROM transactions")
    total_vip = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(service_ppn) FROM transactions")
    total_ppn = cursor.fetchone()[0]
    
    print(f"Total Pendapatan: Rp {total_income:,.2f}")
    print(f"Total Biaya Layanan: Rp {total_service:,.2f}")
    print(f"Total Biaya VIP: Rp {total_vip:,.2f}")
    print(f"Total PPN: Rp {total_ppn:,.2f}")
    print("\n")

# Menu kasir
def cashier_menu():
    while True:
        clear_screen()
        print("\n=== Sistem Kasir Salon - Cashier ===")
        print("1. Tampilkan Database Transaksi")
        print("2. Hapus Transaksi")
        print("3. Tampilkan Laporan Pendapatan")
        print("4. Keluar")
        
        choice = input("Pilih opsi: ")
        clear_screen()
        
        if choice == '1':
            cashier_show_database()
        elif choice == '2':
            delete_transaction()
        elif choice == '3':
            show_income_report()
        elif choice == '4':
            print("Terima kasih telah menggunakan sistem kasir!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")
        
        input("Tekan Enter untuk melanjutkan...")

# Jalankan program
if __name__ == "__main__":
    cashier_menu()
