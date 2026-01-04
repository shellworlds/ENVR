#include <iostream>
#include <vector>
#include <cmath>

class SurveyProcessor {
public:
    void processPoints(const std::vector<std::vector<double>>& points) {
        std::cout << "ENVR9 C++ Survey Processor" << std::endl;
        std::cout << "Processing " << points.size() << " points" << std::endl;
        
        if (points.size() > 0) {
            double minX = points[0][0], maxX = points[0][0];
            double minY = points[0][1], maxY = points[0][1];
            double minZ = points[0][2], maxZ = points[0][2];
            
            for (const auto& point : points) {
                if (point[0] < minX) minX = point[0];
                if (point[0] > maxX) maxX = point[0];
                if (point[1] < minY) minY = point[1];
                if (point[1] > maxY) maxY = point[1];
                if (point[2] < minZ) minZ = point[2];
                if (point[2] > maxZ) maxZ = point[2];
            }
            
            std::cout << "Bounding Box:" << std::endl;
            std::cout << "  X: " << minX << " to " << maxX << std::endl;
            std::cout << "  Y: " << minY << " to " << maxY << std::endl;
            std::cout << "  Z: " << minZ << " to " << maxZ << std::endl;
            std::cout << "  Volume: " << (maxX-minX)*(maxY-minY)*(maxZ-minZ) << std::endl;
        }
    }
};

int main() {
    SurveyProcessor processor;
    std::vector<std::vector<double>> samplePoints = {
        {0, 0, 0},
        {10, 0, 0},
        {10, 10, 0},
        {0, 10, 0},
        {0, 0, 5},
        {10, 0, 5},
        {10, 10, 5},
        {0, 10, 5}
    };
    
    processor.processPoints(samplePoints);
    return 0;
}
