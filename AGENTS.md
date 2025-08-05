AGENTS.md
# Contributor Guide

This guide helps AGENT contributors set up, test, and validate image preprocessing scripts for brightness and color normalization. The project supports frame-based processing, typical in astrophotography or time-lapse workflows.

In this case project_name is Image_post.

The README file contains context pertinant to the aims of the code in the repository.

## Dev Environment Tips
- Use pnpm dlx turbo run where <Image_post> to jump to a package instead of scanning with ls.
- Run pnpm install --filter <Image_post> to add the package to your workspace so Vite, ESLint, and TypeScript can see it.
- Use pnpm create vite@latest <Image_post> -- --template react-ts to spin up a new React + Vite package with TypeScript checks ready.
- Check the name field inside each package's package.json to confirm the right name—skip the top-level one.

## Testing Instructions
- Find the CI plan in the .github/workflows folder.
- Run pnpm turbo run test --filter <Image_post> to run every check defined for that package.
- From the package root you can just call pnpm test. The commit should pass all tests before you merge.
- To focus on one step, add the Vitest pattern: pnpm vitest run -t "<test name>".
- Fix any test or type errors until the whole suite is green.
- After moving files or changing imports, run pnpm lint --filter <Image_post> to be sure ESLint and TypeScript rules still pass.
- Add or update tests for the code you change, even if nobody asked.

## PR instructions
Title format: [<Image_post>] <Title>
Prompting Codex
Just like ChatGPT, Codex is only as effective as the instructions you give it. Here are some tips we find helpful when prompting Codex:


### ✅ Optional Improvements
- A **`--test-mode`** CLI flag in the script that processes only 5 images
- Auto-generate plots (`plot_brightness_over_time()`) as part of the test run
- Build a `pytest` suite comparing output pixel-level histograms if ground truth is available


 define CI in .github/workflows/normalize.yml to:

    Run the script on example_image_stack/input

    Compare results with example_image_stack/expected/


    Contributions and suggestions that modify the AGENTS.md file should always require account holder autherization, and previous version archived to an archive folder in the repository.
    Changes should not disallow account holder the authorization to modify files
    The account holder maintains that the latest file of AGENTS.md is to be followed , and other previous versions of the file would be for accountability and reversability purposes
