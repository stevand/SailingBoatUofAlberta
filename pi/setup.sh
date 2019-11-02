### Script for setting up raspberry py
### bash -i ./setup.sh to run

sudo apt-get update

# Install pyenv requirements
sudo apt-get install python3-pip python3-dev

# Install other useful stuff
sudo apt-get install vim

# Install xsens mti drivers
cd ~
git clone https://github.com/xsens/xsens_mt.git
cd ~/xsens_mt
make
sudo modprobe usbserial
cd ..

Install pyenv
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

# Update bashrc
echo '### Pyenv ###' >> ~/.bashrc
echo $'export PATH="/home/pi/.pyenv/bin:$PATH"' >> ~/.bashrc
echo $'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

# Activate Python 3.6
pyenv install 3.6.0
pyenv exec python -V
pyenv global 3.6.0

# Install python requirements
pip install -r requirements.txt
