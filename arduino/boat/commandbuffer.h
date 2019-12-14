// Class
#include "Arduino.h"

class CommandBuffer
{
private:
    char *buffer;
    int size;
    int i;
    bool ready = false;
    bool shouldClear = false;
    void clearBuffer();
    void addChar(char c);

public:
    CommandBuffer(int size);
    void update();
    char *getCommand();
    bool commandReady();

};