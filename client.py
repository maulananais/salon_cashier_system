import os
from db import cursor, db

# Fungsi untuk membersihkan layar
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Katalog layanan salon
services = {
    1: ('Potong Rambut', {
        1: ('Pendek', 25000),
        2: ('Sedang', 40000),
        3: ('Panjang', 50000)
    }),
    2: ('Creambath', 50000),
    3: ('Hair Spa', 75000),
    4: ('Smoothing', 325000),
    5: ('Coloring', 275000)
}

# Fungsi untuk menampilkan katalog layanan
def show_services():
    print("\nKatalog Layanan Salon:")
    for key, value in services.items():
        if isinstance(value[1], dict):
            print(f"{key}. {value[0]}")
        else:
            print(f"{key}. {value[0]} - Rp {value[1]:,}")

# Fungsi untuk memilih layanan
def choose_service():
    clear_screen()
    show_services()
    
    try:
        service_choice = int(input("Pilih layanan (angka): "))
        clear_screen()
        if service_choice == 1:
            print("Model Potong Rambut:")
            for key, value in services[1][1].items():
                print(f"{key}. {value[0]} - Rp {value[1]:,}")
            hair_choice = int(input("Pilih model potong rambut (angka): "))
            clear_screen()
            if hair_choice in services[1][1]:
                return (f"Potong Rambut - {services[1][1][hair_choice][0]}", services[1][1][hair_choice][1])
            else:
                print("Pilihan tidak valid!")
                return choose_service()
        elif service_choice in services:
            return (services[service_choice][0], services[service_choice][1])
        else:
            print("Pilihan tidak valid!")
            return choose_service()
    except ValueError:
        print("Pilihan tidak valid! Harap masukkan angka.")
        return choose_service()

# Fungsi untuk memilih tipe pelanggan
def choose_customer_type():
    while True:
        print("\nTipe Pelanggan:")
        print("1. Reguler")
        print("2. VIP (+Rp 500,000)")
        try:
            choice = int(input("Pilih tipe pelanggan (1/2): "))
            if choice == 1:
                return "Reguler", 0
            elif choice == 2:
                return "VIP", 500000
            else:
                print("Pilihan tidak valid!")
        except ValueError:
            print("Pilihan tidak valid! Harap masukkan angka.")

# Fungsi untuk menghitung total biaya dengan PPN 11%
def calculate_total(price, vip_fee):
    subtotal = price + vip_fee
    ppn = subtotal * 0.11
    total = subtotal + ppn
    return total, ppn

# Fungsi untuk transaksi Non-Booking
def client_non_book():
    clear_screen()
    client_name = input("Nama pelanggan: ")
    clear_screen()
    customer_type, vip_fee = choose_customer_type()
    clear_screen()
    selected_service = choose_service()
    
    total, ppn = calculate_total(selected_service[1], vip_fee)
    
    clear_screen()
    # Tampilkan rincian transaksi
    print(f"\nRincian Transaksi:\nNama Pelanggan: {client_name}")
    print(f"Tipe Pelanggan: {customer_type}")
    print(f"Layanan: {selected_service[0]}")
    print(f"Biaya Layanan: Rp {selected_service[1]:,}")
    if vip_fee > 0:
        print(f"Biaya VIP: Rp {vip_fee:,}")
    print(f"PPN (11%): Rp {ppn:,.2f}")
    print(f"Total Biaya: Rp {total:,.2f}")
    
    # Simpan ke database
    cursor.execute("INSERT INTO transactions (client_name, service_name, service_price, service_ppn, total_price, is_booking, customer_type, vip_fee) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (client_name, selected_service[0], selected_service[1], ppn, total, False, customer_type, vip_fee))
    db.commit()
    print("\nTransaksi berhasil disimpan!\n")

# Fungsi untuk transaksi Booking
def client_book():
    clear_screen()
    client_name = input("Nama pelanggan: ")
    clear_screen()
    customer_type, vip_fee = choose_customer_type()
    clear_screen()
    selected_service = choose_service()
    
    total, ppn = calculate_total(selected_service[1], vip_fee)
    
    clear_screen()
    # Tampilkan rincian booking
    print(f"\nRincian Booking:\nNama Pelanggan: {client_name}")
    print(f"Tipe Pelanggan: {customer_type}")
    print(f"Layanan: {selected_service[0]}")
    print(f"Biaya Layanan: Rp {selected_service[1]:,}")
    if vip_fee > 0:
        print(f"Biaya VIP: Rp {vip_fee:,}")
    print(f"PPN (11%): Rp {ppn:,.2f}")
    print(f"Total Biaya: Rp {total:,.2f}")
    
    # Simpan ke database
    cursor.execute("INSERT INTO transactions (client_name, service_name, service_price, service_ppn, total_price, is_booking, customer_type, vip_fee) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (client_name, selected_service[0], selected_service[1], ppn, total, True, customer_type, vip_fee))
    db.commit()
    print("\nBooking berhasil disimpan!\n")

# Menu client
def client_menu():
    while True:
        clear_screen()
        print("\n=== Sistem Kasir Salon - Client ===")
        print("1. Client (Non Book)")
        print("2. Client (Book)")
        print("3. Keluar")
        
        choice = input("Pilih opsi: ")
        clear_screen()
        
        if choice == '1':
            client_non_book()
        elif choice == '2':
            client_book()
        elif choice == '3':
            print("Terima kasih telah menggunakan sistem kasir client!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")
        
        input("Tekan Enter untuk melanjutkan...")

# Jalankan program
if __name__ == "__main__":
    client_menu()