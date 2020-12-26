#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <windows.h>
#include <fstream>
#include <sstream>
#include <iostream>

class GraphicFlow : public sf::Drawable, sf::Transformable
{
public:
    bool update(std::string mapFlow, const long int* tileSize, unsigned long int width, unsigned long int height)
    {
        m_vertices.setPrimitiveType(sf::Quads);
        m_vertices.resize(width * height * 4);
        int tileNumber = width * height;
        char currCell;
        int diff;
        sf::Color interim;
        sf::Color color;
        for (unsigned long int n = 0; n < height; ++n)
        {
            for (unsigned long int m = 0; m < width; ++m)
            {
                sf::Vertex* quad = &m_vertices[(n * width + m) * 4];
                quad[0].position = sf::Vector2f(m * tileSize[1], n * tileSize[0]);
                quad[1].position = sf::Vector2f(m * tileSize[1], (n + 1) * tileSize[0]);
                quad[2].position = sf::Vector2f((m + 1) * tileSize[1], (n + 1) * tileSize[0]);
                quad[3].position = sf::Vector2f((m + 1) * tileSize[1], n * tileSize[0]);
                currCell = mapFlow[m + n * width];
                switch (currCell)
                {
                case ',':
                    color = ground;
                    break;
                case '~':
                    color = water;
                    break;
                case '#':
                    color = stone;
                    break;
                case 'S':
                    color = snake;
                    break;
                case 'W':
                    color = weasel;
                    break;
                case 'H':
                    color = hedgehog;
                    break;
                case 'm':
                    color = mouse;
                    break;
                case 'f':
                    color = frog;
                    break;
                case 'b':
                    color = bird;
                    break;
                default:
                    diff = currCell - '0';
                    interim = grass;
                    interim.g -= 5 * diff;
                    interim.r -= 10 * diff;
                    color = interim;
                }
                quad[0].color = color;
                quad[1].color = color;
                quad[2].color = color;
                quad[3].color = color;
            }
        }
        return true;
    }

private:
    sf::Color ground{ 150, 100, 0 };
    sf::Color water{ 0, 50, 150};
    sf::Color stone{ 155, 155, 155 };
    sf::Color grass{100, 150, 20};  
    sf::Color hedgehog{10,10,10};
    sf::Color snake{230,130,120};
    sf::Color weasel{90,50,0};
    sf::Color mouse{185,160,120};
    sf::Color frog{160,210,160};
    sf::Color bird{30,64,110};//',', '~', '#', '1', 'H','S','W','m','f','b'

    sf::VertexArray m_vertices;

    virtual void draw(sf::RenderTarget& target, sf::RenderStates states) const
    {
        states.transform *= getTransform();

        target.draw(m_vertices, states);
    }
};

int main()
{
    ShowWindow(FindWindowA("ConsoleWindowClass", NULL), false);
    std::ifstream pathFile("..\\project_path.txt");
    std::string path;
    pathFile >> path;
    pathFile.close();
    unsigned long int width;
    unsigned long int height;
    std::ifstream flow(path + "buffer.txt");
    flow >> width;
    flow >> height;
    flow.close();
    std::ofstream outflow(path + "buffer.txt");
    outflow.close();
    const long int tileSize[2] = { 8, 8 };
    sf::RenderWindow window(sf::VideoMode(tileSize[0] * width, tileSize[1] * height), "Hunters&Pray");  

    GraphicFlow map;
    
    std::string last = "$";
    std::string mapstr = "$";
    std::string command;

    while (window.isOpen())
    {
        std::ifstream signalFlow(path + "signal.txt");
        signalFlow >> command;
        signalFlow.close();
        if (command == "close")
        {
            window.close();
            break;
        }
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }
        std::ifstream flow(path + "buffer.txt");
        flow >> mapstr;
        flow.close();
        std::ofstream outflow(path + "buffer.txt");
        outflow.close();
        if (mapstr != last)
        {
            window.clear();
            map.update(mapstr, tileSize, width, height);
            window.draw(map);
            window.display();
            last = mapstr;
        }
    }
    FreeConsole();
    return 0;
}