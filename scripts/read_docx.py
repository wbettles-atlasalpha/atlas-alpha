import docx

def get_text(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

print(get_text('/home/warwick/.openclaw/workspace/Livewire-Ultimate-Investing-Guide-2026.docx'))
