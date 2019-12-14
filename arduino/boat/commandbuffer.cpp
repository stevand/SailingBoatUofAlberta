#include "commandbuffer.h"

/**
  * Initializes a buffer for strings sent over Serial, read one char at a time
  * 
  * @param size the length of the longest string that could be sent
*/
CommandBuffer::CommandBuffer(int size) : size(size)
{
    buffer = new char[size + 1];
    clearBuffer();
}

void CommandBuffer::clearBuffer()
{
    i = 0;
    buffer[0] = '\0';
    shouldClear = false;
}

void CommandBuffer::addChar(char c)
{
    buffer[i++] = c;
    buffer[i] = '\0';
}

// Reads a char in from Serial if one is available
void CommandBuffer::update()
{
    if (ready)
    {
        return;
    }

    if (shouldClear)
    {
        clearBuffer();
    }

    if (Serial.available())
    {
        char in = Serial.read();
        if (in == '\n')
        {
            ready = true;
            return;
        }

        if (i == size)
        {
            clearBuffer();
        }

        addChar(in);
    }
}

// Returns the command string stored in the buffer
char *CommandBuffer::getCommand()
{
    ready = false;
    shouldClear = true;
    return buffer;
}

// Returns true if a full command string has been read in
bool CommandBuffer::commandReady()
{
    return ready;
}