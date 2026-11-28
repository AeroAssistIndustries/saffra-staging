# Saffra staging site

**Live staging link: https://aeroassistindustries.github.io/saffra-staging/**

Static staging site for Saffra daily intimacy gummies (working name).

## Views

| View | Link |
| --- | --- |
| Home | https://aeroassistindustries.github.io/saffra-staging/ |
| For her | https://aeroassistindustries.github.io/saffra-staging/#her |
| For him | https://aeroassistindustries.github.io/saffra-staging/#him |
| Find your formula quiz | https://aeroassistindustries.github.io/saffra-staging/#quiz |
| Games for two | https://aeroassistindustries.github.io/saffra-staging/#play |
| Journal and podcast preview | https://aeroassistindustries.github.io/saffra-staging/#journal |
| Ask us | https://aeroassistindustries.github.io/saffra-staging/#ask |
| Creators | https://aeroassistindustries.github.io/saffra-staging/#creators |
| Science | https://aeroassistindustries.github.io/saffra-staging/#science |
| About us | https://aeroassistindustries.github.io/saffra-staging/#about |
| Shipping and returns | https://aeroassistindustries.github.io/saffra-staging/#shipping |
| Privacy policy | https://aeroassistindustries.github.io/saffra-staging/#privacy |
| Terms of use | https://aeroassistindustries.github.io/saffra-staging/#terms |
| Brand kit | https://aeroassistindustries.github.io/saffra-staging/#brand |

## Files

- `index.html` is the whole site.
- `img/` holds the bottle renderings. `fonts/` holds Fraunces and DM Sans.
- Lifestyle photos load from Unsplash.

## Publishing

The live site is served from the `gh-pages` branch. Push `main` to `gh-pages` to update it.

## Not connected yet

- The waitlist form does not save sign-ups.
- The lot lookup has no reports until the first batch ships.
- The Ask us form does not send questions.
- The podcast has no episodes yet.
- The Creators application form does not send.

## Launch switches

Flip these when the real domain and store are ready:

1. `index.html` head: remove the `robots` noindex tag and change the title from "Saffra Staging Site".
2. Replace `https://aeroassistindustries.github.io/saffra-staging/` in the `og:` tags and JSON-LD with the live domain.
3. Social icons in the footer: wrap each `li[data-social]` in a link to the real profile.
4. Forms (waitlist, ask, creators, lot lookup): connect to an email service and remove the "Staging preview" messages.
5. Add the business contact address to the privacy, terms and shipping pages.
6. Connect checkout.

## Pages and SEO build

The site is written as one file, `src/index.html`. `tools/build_pages.py` turns it into real pages
(`/her/`, `/him/`, `/journal/` and so on), each with its own title, description, canonical link,
structured data, plus `sitemap.xml` and `robots.txt`.

    python3 tools/build_pages.py https://YOUR-DOMAIN/ OUTPUT_FOLDER          # hidden from search
    python3 tools/build_pages.py https://YOUR-DOMAIN/ OUTPUT_FOLDER public   # searchable

Edit `src/index.html`, then rebuild. Do not edit the built pages by hand.
