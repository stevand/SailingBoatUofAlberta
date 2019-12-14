class Anemometer
{
private:
    int rvPin, tmpPin;
    float *measurements;
    float total = 0, avg = 0;
    int current = 0;
    long lastMeasurement = 0;

public:
    Anemometer(int rvPin, int tmpPin);
    void update();
    float getWindspeed();
    float getCurrentWindspeed();
};