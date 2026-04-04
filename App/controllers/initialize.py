from .user import create_user
from App.database import db
from .lot import create_lot
from .student import create_student
from .admin import create_admin
from App.models import *

def initialize():
    db.drop_all()
    db.create_all()
    
    create_admin("bob", "bobpass")

    create_lot("GIS Lab", "Medium, capable of having 20 machines", 160000.00)
    create_lot("Government Office Lab", "Medium, capable of having 20 machines", 110000.00)
    create_lot("University Computer Lab", "Medium, capable of having 20 machines", 250000.00)
    create_lot("Data Center", "Medium, capable of having 20 machines", 25000000.00)

    create_student("jack", "20240123", "jackpass")
    create_student("cooper", "20231245", "cooperpass")
    create_student("john", "20229876", "johnpass")
    create_student("tony", "20235678", "tonypass")

    create_student("peper", "20246789", "peperpass")
    create_student("steve", "20242345", "stevepass")
    create_student("clint", "20238901", "clintpass")
    create_student("bruce", "20238902", "brucepass")

    # Lot 1 — Graphics/Design Lab

    # Device Type: Workstation Desktop
    # CPU: Intel Core i9-13900K
    # RAM: 64GB DDR5
    # Screen: 27-inch 4K IPS
    # OS: Windows 11 Pro
    # Storage: 2TB NVMe SSD
    # GPU: NVIDIA RTX 4080
    # I/O Ports: 4x USB-A, 2x USB-C, HDMI 2.1, DisplayPort 1.4
    # Peripherals: Mechanical Keyboard, Ergonomic Mouse, Drawing Tablet
    # Features: Webcam, WiFi 6E, Bluetooth 5.2

    # Lot 2 — Programming/Development Lab

    # Device Type: Laptop
    # CPU: AMD Ryzen 7 7745HX
    # RAM: 32GB DDR5
    # Screen: 15.6-inch FHD 144Hz
    # OS: Windows 11 Pro / Ubuntu 22.04 Dual Boot
    # Storage: 1TB NVMe SSD
    # GPU: NVIDIA RTX 3060
    # I/O Ports: 3x USB-A, 2x USB-C, HDMI 2.0, SD Card Reader
    # Peripherals: Wireless Keyboard, Wireless Mouse, USB Hub
    # Features: Fingerprint Reader, WiFi 6, Bluetooth 5.0

    # Lot 3 — General Purpose Lab

    # Device Type: Desktop PC
    # CPU: Intel Core i5-13400
    # RAM: 16GB DDR4
    # Screen: 24-inch FHD
    # OS: Windows 11 Home
    # Storage: 512GB NVMe SSD
    # GPU: Intel UHD Graphics 730
    # I/O Ports: 4x USB-A, 1x USB-C, HDMI 1.4, VGA
    # Peripherals: Standard Keyboard, Optical Mouse
    # Features: Webcam, WiFi 5, Bluetooth 4.2

    # Lot 4 — Data Science/AI Lab

    # Device Type: High-Performance Workstation
    # CPU: AMD Ryzen Threadripper 7960X
    # RAM: 128GB DDR5 ECC
    # Screen: Dual 32-inch 4K
    # OS: Ubuntu 22.04 LTS
    # Storage: 4TB NVMe SSD RAID
    # GPU: NVIDIA RTX 4090 x2
    # I/O Ports: 6x USB-A, 4x USB-C, 2x Thunderbolt 4, Dual Ethernet
    # Peripherals: Ergonomic Keyboard, Precision Mouse, USB-C Docking Station
    # Features: 10GbE Network Card, WiFi 6E, Bluetooth 5.2, Liquid Cooling
