import os
import re

base_dir = r"g:\マイドライブ\AI_work\note_webtoon_gem\pipeline_gems"
files = ["hearing_form_essay.html", "hearing_form_review.html", "hearing_form_story.html"]

css_to_add = """
    details.example-box summary {
      cursor: pointer;
      font-weight: 700;
      color: #a78bfa;
      outline: none;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    details.example-box summary::-webkit-details-marker {
      display: none;
    }
    details.example-box summary::before {
      content: '▼';
      font-size: 0.8rem;
      transition: transform 0.2s;
    }
    details.example-box:not([open]) summary::before {
      transform: rotate(-90deg);
    }
    details.example-box[open] summary {
      margin-bottom: 12px;
      padding-bottom: 12px;
      border-bottom: 1px dashed rgba(255, 255, 255, 0.1);
    }"""

for fname in files:
    fpath = os.path.join(base_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # Avoid duplicate CSS injection
    if "details.example-box summary" not in content:
        # We find `.example-box { ... }` and append the new rules right after it
        content = re.sub(
            r'(\.example-box\s*\{[^}]*\})',
            r'\1' + css_to_add,
            content
        )

    # We want to replace <div class="example-box"> with <details class="example-box" open><summary>...
    content = content.replace('<div class="example-box">', '<details class="example-box" open>\n          <summary>💡 回答例を表示 / 非表示</summary>')
    content = content.replace('<div class="example-box" >', '<details class="example-box" open>\n          <summary>💡 回答例を表示 / 非表示</summary>')
    
    # We must replace the corresponding closing </div> with </details>.
    # They usually look like:
    #         </div>
    #         <input
    content = re.sub(r'(<details class="example-box" open>.*?)\n        </div>', r'\1\n        </details>', content, flags=re.DOTALL)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

print("Done updating HTML files.")
