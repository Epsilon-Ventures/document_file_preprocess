from googleapiclient.errors import HttpError
import json
import re

def __read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    text = text_run.get('content')
    if len(text) > 40:
        return text
    return re.sub(r'\n*\d?\n', '\t', text)


def __read_structural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += __read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text +=  __read_structural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += __read_structural_elements(toc.get('content'))
    
    return text+'\n'

def get_docs_contents(service, document_id, get="text"):
    try:
        # Retrieve the documents contents from the Docs service.
        document = service.documents().get(documentId=document_id).execute()
        doc_content = document.get('body').get('content')

        if get == "json":
            with open('./ques/ques.json', 'w') as file:
                doc_json = json.dumps(doc_content)
                file.write(doc_json)

        elif get == 'text':
            with open('./ques/ques.txt', 'w') as file:
                file.write(__read_structural_elements(doc_content))

    except HttpError as err:
        print(err)