#!/bin/sh

# Install packages after installing base Debian with no GUI


# xorg display server installation
sudo apt install -y xorg xinit arandr

# Python,make,git
sudo apt install -y python3-pip gcc python3-dev make

# Microcode for Intel/AMD
# sudo apt install -y amd64-microcode
sudo apt install -y intel-microcode

# Qtile requirements
sudo apt install -y libpangocairo-1.0-0
sudo apt install -y python3-xcffib python3-cairocffi

# Remove Python /usr/lib/python3.x/EXTERNALLY-MANAGED
sudo rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED

# Install qtile
git clone https://github.com/qtile/qtile
cd qtile
pip3 install .

# File Manager
sudo apt install -y pcmanfm ranger ueberzug udiskie

# Install Nextcloud Client
sudo apt install -y nextcloud-desktop

# System Tools
sudo apt install -y dialog mtools dosfstools avahi-daemon acpi acpid gvfs-backends xfce4-power-manager build-essential libpam0g-dev libxcb-xkb-dev

sudo systemctl enable avahi-daemon
sudo systemctl enable acpid

# Terminal and Terminal apps
sudo apt install -y alacritty exa

# Audio Utils
sudo apt install -y alsa-utils pavucontrol

# System Info Utils
sudo apt install -y neofetch htop

# Printingi and bluetooth 
sudo apt install -y cups
sudo apt install -y bluez blueman

# sudo systemctl enable bluetooth
sudo systemctl enable cups

# Browser Installation
sudo apt install -y chromium

# Image Handlers
sudo apt install -y feh nitrogen flameshot

# Window Manager Utils
sudo apt install -y picom sxhkd rofi

# Terminal IDE
sudo apt install -y neovim

# Install fonts and papirus icon theme
sudo apt install -y fonts-jetbrains-mono papirus-icon-theme textlive-fonts-extra fonts-roboto fonts-hanazono

# Install zsh and zsh tools
sudo apt install -y zsh zsh-syntax-highlighting zsh-autosuggestions

# Move dotfiles
cd ~/dotfiles
cp .zshenv ~/
cp -r alacritty bspwm neofetch nvim polybar qtile ranger rofi sxhkd zsh ~/.config

# Install ly 
cd ~
git clone --recurse-submodules https://github.com/fairyglade/ly
cd ly
make
sudo make install installsystemd
sudo systemctl enable ly.service

# Adding qtile.desktop to xsessions directory
cat > ./temp << "EOF"
[Desktop Entry]
Name=Qtile
Comment=Qtile Session
Exec=qtile start
Type=Application
Keywords=wm;tiling
EOF
sudo cp ./temp /usr/share/xsessions/qtile.desktop;rm ./temp
u=$USER
sudo echo "Exec=/home/$u/.local/bin/qtile start" | sudo tee -a /usr/share/xsessions/qtile.desktop

# Change Shell
chsh -s $(which zsh)

printf "\e[1;32mDone! you can now reboot.\e[0m\n"
