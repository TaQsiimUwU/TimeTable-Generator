#include<iostream>
#include <map>
#include<string>
#include <vector>
struct TimeSlots;
using namespace std;

struct Course
{
    int id;
    string name;
    string code;
    bool hasLab  = false;
    bool isGP = false;
    string lecIns = "";
    string labIns = "";
};

struct Professor
{
    int id;
    string name;
    vector<int> qualifiedCourses;
    vector<int> busyTimeSlots;
};
struct TA
{
    int id ;
    string name;
    vector<int> qualifiedCourseLabs;
    map<TimeSlots , bool> assignedTimeSlots ;
};
enum RoomType
{
    LabCs = 0 ,
    LabPHY = 1 ,
    LabDIG = 2 ,
    ClassRoom = 3 ,
    Theater = 4,
    Hall = 5
};
struct Rooms
{
    int id;
    string code;
    int capacity;
    RoomType type ;
    bool isBusy = false;
};

struct TimeSlots
{
    string day ;
    int timeSlotIndex;
    bool isBusy = false;
};

int main()
{

}