#!/bin/python3

# Regenerating the zip package after environment reset
import zipfile
import os

# Directory and file content setup
base_path = "/wnq/wnq_initpaq"
os.makedirs(base_path, exist_ok=True)

# Script to remount /box and /rec
remount_script = """#!/bin/bash
# Activate and mount box and rec after proxmox install

# wnq
WNQ_BASE="/wnq"
WNQ_PACK="/wnq/wnq_initpaq"

# box
BOX_MNT="/box"
BOX_PV1="/dev/sda1"
BOX_PV2="/dev/sdb1"
BOX_VG="boxvg"
BOX_LV="boxlv"
BOX_DEV="/dev/boxvg/boxlv"

# rec
REC_MNT="/rec"
REC_PV1="/dev/sdc1"
REC_PV2="/dev/sdd1"
REC_VG="recvg"
REC_LV="reclv"
REC_DEV="/dev/recvg/reclv"

echo "Activating LVM volumes..."
lvchange -ay "${BOX_VG}/${BOX_LV}"
lvchange -ay "${REC_VG}/${REC_LV}"

echo "Creating mount points..."
mkdir -p "${BOX_MNT}"
mkdir -p "${REC_MNT}"

echo "Mounting volumes..."
mount "${BOX_DEV}" "${BOX_MNT}"
mount "${REC_DEV}" "${REC_MNT}"

echo "Box device "${BOX_DEV}" is now mounted to "${BOX_MNT}"
echo "Rec device "${REC_DEV}" is now mounted to "${REC_MNT}"
echo "Done re-mounting our wonqstaq data!"
"""

# Template info for Proxmox VM
vm_template = """# wonqstaq-infra - vm_template
#
# Proxmox VM Template: Node with bind-mounted /box and /rec

VM Name: wonq-node0
vCPUs: 8
RAM: 32768 MB
Disks:
  - Primary OS disk (from template or ISO)
  - Host bind: /wnq → /data/wnq
  - Host bind: /box → /data/box
  - Host bind: /rec → /data/rec
Network:
  - Bridge: vmbr0
"""

# File paths
remount_script_path = os.path.join(base_path, "wonqstaq-data-remount.sh")
vm_template_path = os.path.join(base_path, "wonqstaq-vm-template.txt")

# Write files
with open(remount_script_path, "w") as f:
    f.write(remount_script)
os.chmod(remount_script_path, 0o755)

with open(vm_template_path, "w") as f:
    f.write(vm_template)

# Create zip archive
zip_path = "/wnq/wnq_initpaq.zip"
with zipfile.ZipFile(zip_path, "w") as zipf:
    zipf.write(remount_script_path, arcname="wonqstaq-data-remount.sh")
    zipf.write(vm_template_path, arcname="wonqstaq-vm-template.txt")

zip_path
