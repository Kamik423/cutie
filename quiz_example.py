import cutie

q = ['First Question',
        'One',
        'Two',
        'Three']

q2 = ['Second Question',
        'Four',
        'Five',
        'Six']

q3 = "Yes or no"

qlist = [q, q2, q3]
qtype = ['select_multiple', 'select', 'prompt_yes_or_no']

cap = [[0], [0]]
print(qlist)
cutie.quiz(questions = qlist, question_types = qtype, caption_indices = cap,
            newlines = 1, 
            path='quiz_write_example.txt')
