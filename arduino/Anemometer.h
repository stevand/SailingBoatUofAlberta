class Anemometer {
    private:
        int rvPin, tmpPin;
    public:
        Anemometer(int rvPin, int tmpPin);

        float getWindspeed();

}