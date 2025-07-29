#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "json.hpp"
#include <fstream>
#include <iostream>

namespace py = pybind11;
using json = nlohmann::json;

std::string combine(const std::vector<std::string> &tact_paths, const std::vector<float> &intensities, const std::string &base_file_path)
{
    std::ifstream f_base(base_file_path);
    if (!f_base)
        throw std::runtime_error("Impossible d'ouvrir COMBINAISON.tact");
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
            std::cout << "Traitement du fichier : " << path << std::endl;
            try
            {
                auto &front_points = track["effects"][0]["modes"]["VestFront"]["pathMode"]["feedback"][0]["pointList"];
                auto &back_points = track["effects"][0]["modes"]["VestBack"]["pathMode"]["feedback"][0]["pointList"];
                for (size_t j = 0; j < std::min(front_points.size(), back_points.size()); ++j)
                {
                    front_points[j]["intensity"] = intensities[incr];
                    back_points[j]["intensity"] = intensities[incr];
                }
            }

            catch (...)
            {
                continue;
            }

            try
            {
                auto &front_points = track["effects"][0]["modes"]["VestFront"]["dotMode"]["feedback"][0]["pointList"];
                auto &back_points = track["effects"][0]["modes"]["VestBack"]["dotMode"]["feedback"][0]["pointList"];
                for (size_t j = 0; j < std::min(front_points.size(), back_points.size()); ++j)
                {
                    front_points[j]["intensity"] = intensities[incr];
                    back_points[j]["intensity"] = intensities[incr];

                    std::cout << "fr " << front_points[j]["intensity"] << "\n"
                              << "bck" << back_points[j]["intensity"] << std::endl;
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
    m.doc() = "Module de fusion .tact optimisé en C++";
    m.def("combine", &combine, "Combine plusieurs fichiers .tact");
}
