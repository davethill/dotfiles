#!/bin/sh

# Install packages after installing base Arch with no GUI

# Create .config folder
mkdir ~/.config

# xorg display server installation
sudo pacman -S --noconfirm xorg arandr

# Python,make,git
sudo pacman -S --noconfirm python3 python-pip make git

# Microcode for Intel/AMD 
# sudo pacman -S --noconfirm amd64-microcode
# sudo pacman -S --noconfirm intel-microcode 

# File Manager 
sudo pacman -S --noconfirm pcmanfm ranger ueberzug udiskie

# Install Nextcloud Client
sudo pacman -S --noconfirm nextcloud-client 

# System Tools
sudo pacman -S --noconfirm dialog mtools dosfstools avahi nss-mdns acpi acpid gvfs nfs-utils ntfs-3g network-manager-applet unzip base-devel rust

sudo systemctl enable avahi-daemon
sudo systemctl enable acpid

# Terminal and Terminal apps
sudo pacman -S --noconfirm alacritty starship exa

# Audio Utils
sudo pacman -S --noconfirm alsa-utils pavucontrol 

# System Info Utils
sudo pacman -S --noconfirm neofetch htop 

# Printing
sudo pacman -S --noconfirm cups

sudo systemctl enable cups

# Browser Installation 
sudo pacman -S --noconfirm chromium 

# Image Handlers 
sudo pacman -S --noconfirm feh nitrogen flameshot

# Window Manager Utils
sudo pacman -S --noconfirm picom sxhkd rofi 

# Terminal IDE
sudo pacman -S --noconfirm neovim

# Install fonts and papirus icon theme 
sudo pacman -S --noconfirm ttf-jetbrains-mono-nerd papirus-icon-theme ttf-nerd-fonts-symbols-common ttf-noto-nerd ttf-opensans ttf-roboto ttf-hanazono

# Install zsh and zsh tools
sudo pacman -S --noconfirm zsh zsh-syntax-highlighting zsh-autosuggestions zsh-completions

# Qtile Install 
sudo pacman -S --noconfirm qtile


# Move dotfiles
cd ~/dotfiles
cp .zshenv ~/
cp -r alacritty bspwm neofetch nvim polybar qtile ranger rofi sxhkd zsh ~/.config

# Set up AUR
cd ~
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si --noconfirm

# System Info Utils from Paru
paru -S --noconfirm nitch ly-git

# Enable lightdm
sudo systemctl enable ly.service

# PIP Install psutil for Qtile Widgets
pip install psutil

# Change Shell
chsh -s $(which zsh)

printf "\e[1;32mDone! you can now reboot.\e[0m\n"
