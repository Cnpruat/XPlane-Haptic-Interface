#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "json.hpp"
#include <fstream>

namespace py = pybind11;
using json = nlohmann::json;

std::string combine(const std::vector<std::string> &tact_paths, const std::vector<float> &intensities, const std::string &base_file_path)
{
    std::ifstream f_base(base_file_path);
    if (!f_base)
        throw std::runtime_error("Unable to open BLANK.tact");
    json combined = json::parse(f_base);

    size_t incr = 0;
    for (const auto &path : tact_paths)
    {
        std::ifstream f(path);
        if (!f)
            continue;
        json data = json::parse(f);
        auto &tracks = data["project"]["tracks"];

        for (auto &track : tracks)
        {
            // We use 4 try because the patterns will sometimes use pathMode or dotMode and  because the
            // patterns will sometimes be on the front of the vest, sometime on the back and sometime on both.
            try
            {
                auto &front_points = track["effects"][0]["modes"]["VestFront"]["pathMode"]["feedback"][0]["pointList"];
                for (auto &pt : front_points)
                {
                    pt["intensity"] = intensities[incr];
                }
            }
            catch (...)
            {
                continue;
            }

            try
            {
                auto &back_points = track["effects"][0]["modes"]["VestBack"]["pathMode"]["feedback"][0]["pointList"];
                for (auto &pt : back_points)
                {
                    pt["intensity"] = intensities[incr];
                }
            }
            catch (...)
            {
                continue;
            }

            try
            {
                auto &front_points = track["effects"][0]["modes"]["VestFront"]["dotMode"]["feedback"][0]["pointList"];
                for (auto &pt : front_points)
                {
                    pt["intensity"] = intensities[incr];
                }
            }
            catch (...)
            {
                continue;
            }

            try
            {
                auto &back_points = track["effects"][0]["modes"]["VestBack"]["dotMode"]["feedback"][0]["pointList"];
                for (auto &pt : back_points)
                {
                    pt["intensity"] = intensities[incr];
                }
            }
            catch (...)
            {
                continue;
            }
        }

        combined["project"]["tracks"].insert(
            combined["project"]["tracks"].end(), tracks.begin(), tracks.end());

        incr++;
    }

    std::string out_path = "./python_interface/combine/combined_output.tact";
    std::ofstream out(out_path);
    out << combined.dump();
    return out_path;
}

PYBIND11_MODULE(tactcombine, m)
{
    m.doc() = "Optimized .tact file merging library for python in C++";
    m.def("combine", &combine, "Combine several .tact files and edit their intensity");
}
