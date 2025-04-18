#!/bin/python3

# modules
import os
from fpdf import FPDF

# make sure /wnq exists
os.makedirs("/wnq", exist_ok=True)

# pdf config
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "wonqstaq proxmox setup & wonqstaq data remount guide", ln=True, align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("Courier", "", 10)
        self.multi_cell(0, 6, body)
        self.ln()

pdf = PDF()
pdf.add_page()

# overview
pdf.chapter_title("Overview")
pdf.chapter_body(
    "This guide outlines the steps to install Proxmox VE on a Hetzner SX65 server using only the 1TB NVMe disk, "
    "while preserving the 4x 20TB disks currently used for /box and /rec mounted via LVM."
)

# proxmox install
pdf.chapter_title("1. Prepare Install Media")
pdf.chapter_body(
    "- Download latest Proxmox VE ISO from https://www.proxmox.com/en/downloads\n"
    "- Flash ISO to USB with:\n"
    "  sudo dd if=proxmox-ve_*.iso of=/dev/sde bs=4M status=progress && sync"
)

pdf.chapter_title("2. Install Proxmox on NVMe Only")
pdf.chapter_body(
    "- During install, choose manual setup\n"
    "- Use only /dev/nvme0n1 and /dev/nvme1n1\n"
    "- Suggested partition layout on /dev/nvme0n1:\n"
    "  * boot    (1GB)\n"
    "  * efi     (1GB)\n"
    "  * opt   (200GB)\n"
    "  * var   (500GB)\n"
    "- Suggested partition layout on /dev/nvme1n1:\n"
    "  * home  (198GB)\n"
    "  * etc   (100GB)\n"
    "  * usr   (200GB)\n"
    "  * www   (500GB)\n"
    "- DO NOT touch /dev/sda, /dev/sdb, /dev/sdc, or /dev/sdd and/or their partitions (/dev/sdaX, /dev/sdbX, /dev/sdcX and /dev/sddX"
)

# remount data
pdf.chapter_title("3. Re-mount Data Disks After Install")
pdf.chapter_body(
    "- Boot Proxmox and SSH in\n"
    "- Run:\n"
    "  sudo pvs\n"
    "  sudo vgs\n"
    "  sudo lvs\n"
    "- Mount volumes:\n"
    "  sudo mkdir /mnt/box\n"
    "  sudo mkdir /mnt/rec\n"
    "  sudo lvchange -ay boxvg/boxlv\n"
    "  sudo lvchange -ay recvg/reclv\n"
    "  sudo mount /dev/boxvg/boxlv /mnt/box\n"
    "  sudo mount /dev/recvg/reclv /mnt/rec"
)

# passthrough
pdf.chapter_title("4. Optional: Pass into VMs")
pdf.chapter_body(
    "- Bind mount into container or VM\n"
    "- Or use LVM passthrough:\n"
    "  * WebUI > VM > Hardware > Add > LVM volume\n"
)

# pdf export
pdf_output_path = "/wnq/proxmox_setup_and_wonqstaq_data_remount_guide.pdf"
pdf.output(pdf_output_path)
pdf_output_path
