<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">API server for CoreMl Stable Diffusion</h3>

  <p align="center">
    This is Stable Diffusion CoreML version, working on Mac M series processors with Flask API
    <br />
    <a href="https://github.com/apple/ml-stable-diffusion">The original implementation of <strong>CoreML Stable Diffusion</strong> by Apple</a>
    <br />
    <br />
    ·
    <a href="https://github.com/dvorson/mac_m1_coreml_stable_diffusion_flask_api/issues">Report Bug</a>
    ·
    <a href="https://github.com/dvorson/mac_m1_coreml_stable_diffusion_flask_api/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

First you need to download a model with download_model.py
* npm
  ```sh
  python3 download_model.py
  ```
If you choose non-default model - make sure that model_version, repo_id and mlpackages_dir match between download_model.py and flask_api.py
More on models in <a href="https://github.com/apple/ml-stable-diffusion">the original docs</a>

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/dvorson/mac_m1_coreml_stable_diffusion_flask_api.git
   ```
2. Create virtual env 
   ```sh
   python3 -m venv /path/to/new/virtual/environment
   ```
3. Install python packages
   ```sh
   pip3 install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

When a server is up, send a POST request to localhost:3000/app/inference with the prompt payload:
```json
{
    "prompt": "a painting of a spaceship by basquiat, intricate detail"
}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
