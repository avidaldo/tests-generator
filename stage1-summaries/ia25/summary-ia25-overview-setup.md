<!-- markdownlint-disable MD025 -->

# File Inventory

| # | File | Type | Relevant |
| --- | --- | --- | --- |
| 1 | README.md | `.md` | ✅ |
| 2 | setup/conda_tutorial.md | `.md` | ✅ |
| 3 | setup/py_dependencies.md | `.md` | ✅ |
| 4 | setup/setup.md | `.md` | ✅ |
| 5 | setup/uv_tutorial.md | `.md` | ✅ |

# Content

## [Source: README.md]

### Course map and topic progression

The file presents the course as a collection of notes and examples for Artificial Intelligence in 2024/25. It organizes the material into a progression rather than a flat list.

The route starts with conceptual background on AI, machine learning, neural networks, and generative or agentic AI. It then moves into basic setup and tools, including the overview of technologies for Python AI development.

After setup, the course introduces core Python data tools through NumPy and Pandas notebooks, followed by classic machine-learning algorithms such as linear regression, logistic regression, K-means, KNN, decision trees, Q-learning, and random forests.

The file also identifies a second layer of material centered on complete workflows and complete projects. Workflow notebooks cover train/test thinking, evaluation, pipelines, clustering, and SVM-based image classification. Project links point students toward end-to-end regression, classification, and computer-vision repositories, showing that the course is meant to move from isolated concepts toward integrated applications.

### External repositories and complementary materials

The README signals that several learning units live outside this repository. These include a tic-tac-toe progression, complete projects on California housing, thyroid classification, King County regression, computer vision with OpenCV and YOLO, and LLM-oriented projects such as chat guardrails and RAG.

The important contextual point is that the course expects students to move across repositories while keeping a coherent learning sequence: foundations, tools, algorithms, workflows, and full projects.

## [Source: setup/setup.md]

### Python as the dominant language for AI programming

Python is presented as the main language for machine learning and the one used throughout the course. The reasons given are its high-level and general-purpose nature, its ease of learning, and especially its broad ecosystem of libraries and frameworks for AI, machine learning, and deep learning.

### Other relevant languages in AI

The file distinguishes Python's dominant role from the roles of other languages:

- R is associated primarily with statistics and data analysis.
- C and C++ matter because many Python-accessed libraries are implemented in them for speed and low-level performance.
- Julia is presented as a high-performance language for scientific and technical computing.
- Mojo is described as aiming to combine Python-like usability with C-like performance.

This comparison frames Python as the practical default, while reminding students that performance-critical or statistics-heavy ecosystems still matter.

### Git and Git forges

Git is defined as a distributed version-control system for tracking source-code changes. Git forges are introduced as cloud services for hosting Git repositories, with GitHub, GitLab, and Bitbucket named as examples.

The file stresses that Git and GitHub will be used extensively throughout the course, which makes version control part of the working environment rather than an optional extra.

### IDEs and development environments

The source presents four common environments for Python-based AI work:

- VS Code as a cross-platform source-code editor with wide language support and strong popularity.
- Cursor as a VS Code fork focused on LLM-assisted programming.
- PyCharm as a widely used Python IDE.
- DataSpell as a JetBrains IDE specialized in data analysis.

The file does not claim one universal winner. Instead, it frames these tools as common options inside the Python AI ecosystem.

### Jupyter notebooks and their role

Jupyter is introduced as a browser-based environment for notebooks that combine code, rich text, equations, and visualizations. Python notebooks use the `.ipynb` format, which the file explicitly notes is internally JSON.

This matters because notebooks are positioned not just as code containers but as hybrid explanation-and-execution documents.

### Virtual environments and dependency isolation

Virtual environments are explained as a way to isolate project dependencies from the operating system and from other projects. The key problem they solve is version conflict: different projects may require different versions of the same library.

The file states that the course will mainly use `uv`, describing it as a more recent and modern tool for managing environments and dependencies in Python projects.

### Google Colab

Google Colab is presented as a free cloud environment for running notebooks in Python, R, and other languages, with access to accelerators such as GPUs and TPUs. The implied decision criterion is convenience and cloud execution when local resources are limited or acceleration is needed.

## [Source: setup/py_dependencies.md]

### Why dependency management matters

The file explains the historical growth of Python dependency-management tooling through the problem of dependency hell: version conflicts make projects difficult to maintain and deploy, especially when different projects need different versions of the same libraries.

### Pip as the standard package manager

`pip` is presented as the standard package manager for installing packages from PyPI. It uses `requirements.txt` to record needed libraries and versions for environment reproduction.

The file preserves both sides of the trade-off:

- Advantages: lightweight, simple, flexible, and broadly compatible.
- Limitations: it does not manage virtual environments by itself, and it does not by itself guarantee fully reproducible installations through a lock file in the way newer tools do.

The source also notes that the newer dependency resolver introduced in `pip 20.3` improved conflict handling, which matters as a historical improvement rather than as a complete solution.

### Virtualenv and venv for isolation

The file explains that `virtualenv` and later `venv` solve dependency isolation by creating project-specific environments. `venv`, added in Python 3.3, is presented as the lighter standard option integrated into Python itself.

The conceptual teaching point is separation of concerns: `pip` installs packages, while `venv` isolates environments. Together they provide a workable basic workflow.

### Conda as integrated environment and package management

`Conda` is described as a 2012 tool from the Anaconda ecosystem that manages both environments and packages in an integrated way, including non-Python dependencies.

Its major strengths for machine learning are explicit:

- integrated virtual-environment management,
- precompiled packages,
- strong support for data-science and machine-learning libraries,
- easier handling of complex non-Python dependencies such as compiled C or CUDA-related components.

Its limitations are also preserved:

- heavier disk footprint,
- slower performance than more lightweight or modern alternatives,
- unnecessary complexity for small projects using only basic Python packages.

### Pipenv, Poetry, and uv as later integrated tooling

The file presents Pipenv and Poetry as attempts to provide a more unified and reproducible workflow. Pipenv introduces a lockfile-based environment model, while Poetry is presented as more comprehensive because it uses `pyproject.toml`, manages dependency resolution robustly, and supports building and publishing packages.

### uv as the next-generation fast tool

`uv` is described as a Rust-based installer and resolver designed to replace or accelerate the slowest parts of Python package management.

The key claims preserved are:

- extreme speed, often framed as 10 to 100 times faster than older tools,
- integrated environment management,
- compatibility with Python standards such as `requirements.txt` and `pyproject.toml`,
- ability to complement tools like Poetry rather than necessarily replacing them.

The file frames its impact as a large improvement in developer and CI/CD efficiency.

### Comparison logic and tool-choice criteria

The source compares four main approaches: `pip` plus `venv`, `conda`, `Poetry`, and `uv`.

The decision criteria are explicit:

- use `pip` plus `venv` for simple projects and for learning the basics of isolation,
- use `conda` when machine-learning or data-science work involves complex dependencies, especially non-Python ones,
- use `Poetry` for robust application or library development with broader project-management needs,
- use `uv` when speed and modern dependency workflows are the priority, whether standalone or integrated with Poetry.

This file is one of the clearest sources of context-dependent tool choice in the setup material.

## [Source: setup/conda_tutorial.md]

### Installation and setup

The tutorial recommends Miniconda instead of the full Anaconda distribution because it is smaller and faster to install. The installation process is procedural:

1. Download the installer appropriate to the operating system.
2. Run the installer and allow conda initialization so the terminal recognizes it.
3. Verify the installation by checking the conda version in a new terminal.

### Creating and activating environments

The file defines a conda environment as a directory containing a specific collection of installed packages. It recommends specifying the Python version when creating an environment and notes that packages such as NumPy, pandas, and Jupyter can be installed at environment-creation time.

The operational sequence is explicit: create an environment, activate it before use, and deactivate it to return to the base environment.

### Listing and removing environments

The tutorial shows that users should be able to inspect all existing environments, identify the active one, and deactivate an environment before removing it completely.

### Package management workflow

With an environment active, the tutorial presents the main package operations:

- install packages,
- pin a package to a specific version,
- install from alternative channels such as `conda-forge`,
- list installed packages,
- update one package or all packages,
- remove packages.

The central idea is that environment activation scopes these operations to the correct project context.

### Sharing environments reproducibly

The file presents a reproducibility workflow based on exporting an environment to `environment.yml` and recreating it elsewhere from that file. The important teaching point is that environment sharing is not ad hoc; it should be captured as a formal specification file.

## [Source: setup/uv_tutorial.md]

### Installation and verification

The tutorial presents several installation routes for `uv`, including shell-based installation on macOS and Linux, PowerShell-based installation on Windows, and installation through `pip` when Python is already available.

Verification is treated as a distinct step: users should confirm the tool is installed before depending on it.

### Virtual-environment management with uv

`uv` is presented as integrating the role traditionally split between package managers and environment managers. The tutorial shows that a virtual environment can be created in `.venv`, tied to a specific Python version if needed, activated through platform-specific scripts, and removed simply by deleting the environment directory once it is no longer active.

### Project initialization with pyproject.toml

The tutorial treats `pyproject.toml` as the modern standard for dependency management, preferred over `requirements.txt` for new projects. Students are shown two paths:

- initialize a brand-new project,
- initialize an existing directory by creating the project configuration in place.

### Adding, removing, listing, and syncing dependencies

The tutorial explains that `uv add` both installs packages and updates project metadata, while also creating or updating `uv.lock` for reproducible builds. It distinguishes normal dependencies from development dependencies.

The workflow then expands to package removal, listing installed packages, and using `uv sync` to ensure the environment matches the declared project state.

### Running code through uv

The file highlights one of `uv`'s ergonomic advantages: code, modules, and installed tools can be run without manually activating the environment first. This reduces friction and makes the project environment the default execution context.

### Sharing and reproducing projects

The reproducibility workflow is centered on keeping both `pyproject.toml` and `uv.lock` under version control, then recreating the environment with `uv sync` after cloning the repository.

### Working with legacy requirements files

The tutorial preserves an important compatibility caveat: although `uv` supports legacy `requirements.txt` workflows, migrating to `pyproject.toml` is recommended for better dependency management.

# Cross-References

## Comparisons and distinctions

- Python is positioned as the practical default language for AI development, while R is framed around statistics, C and C++ around performance-critical implementations, Julia around scientific computing, and Mojo around a newer attempt to combine Python usability with low-level speed. [Source: setup/setup.md]
- `pip` plus `venv` separates package management from environment isolation, while `conda` integrates both and also manages non-Python dependencies. [Source: setup/py_dependencies.md; Source: setup/conda_tutorial.md]
- `Poetry` is presented as broader project management around `pyproject.toml`, while `uv` is presented as a high-speed environment and dependency tool that can either stand alone or complement Poetry. [Source: setup/py_dependencies.md; Source: setup/uv_tutorial.md]
- `requirements.txt`, `environment.yml`, and `pyproject.toml` correspond to different reproducibility styles: basic pip workflows, conda environment export, and modern Python project configuration respectively. [Source: setup/py_dependencies.md; Source: setup/conda_tutorial.md; Source: setup/uv_tutorial.md]
- Local virtual environments and Google Colab solve different problems: local isolation and reproducibility versus browser-based execution with access to cloud hardware. [Source: setup/setup.md]

## Dependencies and prerequisites

- The setup material acts as the infrastructure layer for the rest of the ia25 course: background concepts feed into algorithms and workflows, but these setup files define the tools needed to run those materials. [Source: README.md; Source: setup/setup.md]
- Understanding virtual environments is a prerequisite for using any dependency-management workflow safely, whether the chosen tool is `venv`, `conda`, or `uv`. [Source: setup/setup.md; Source: setup/py_dependencies.md]
- The `uv` tutorial depends conceptually on the dependency-management overview because it assumes the reader understands why reproducible project metadata and environment isolation matter. [Source: setup/py_dependencies.md; Source: setup/uv_tutorial.md]
- The conda tutorial is a procedural instantiation of the higher-level argument in favor of integrated environment and package management for data science and machine learning. [Source: setup/py_dependencies.md; Source: setup/conda_tutorial.md]

## Decision criteria and context-dependent choices

- Choose `pip` plus `venv` for beginners and simple scripts when learning the fundamentals of dependency isolation matters more than integrated tooling. [Source: setup/py_dependencies.md]
- Choose `conda` when machine-learning or data-science projects depend on complex compiled or non-Python packages and installation convenience outweighs footprint and speed costs. [Source: setup/py_dependencies.md; Source: setup/conda_tutorial.md]
- Choose `Poetry` when the project needs broader lifecycle management such as robust dependency resolution, packaging, and publishing. [Source: setup/py_dependencies.md]
- Choose `uv` when fast installs, fast resolution, modern `pyproject.toml` workflows, and low-friction local execution are priorities. [Source: setup/setup.md; Source: setup/py_dependencies.md; Source: setup/uv_tutorial.md]
- Use Google Colab when browser-based notebook execution and access to GPUs or TPUs are more important than local environment control. [Source: setup/setup.md]
