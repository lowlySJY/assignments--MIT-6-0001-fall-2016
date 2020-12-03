# Problem Set 4A
# Name: jinyi
# Collaborators:
# Time Spent: 202011301949-2139

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # pass #delete this line and replace with your code here
    assert sequence != '', 'sequnce can not be empty'
    seq = []
    seq.append(sequence)
    per_next = sequence
    if len(per_next) == 1:
        return seq
    else:
        s = sequence[0]
        per_next = sequence[1:]
        sub_seq = get_permutations(per_next)
        new_seq = []
        for i in sub_seq:
            length = len(i) + 1
            for j in range(length):
                new_seq.append(i[0:j] + s + i[j:length])
        # substract repeat
        fin_seq = []
        for i in new_seq:
            if i not in fin_seq:
                fin_seq.append(i)
        return sorted(fin_seq)
        

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    # pass #delete this line and replace with your code here

    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('  Actual Output:', get_permutations(example_input))
    
    example_input = 'ac'
    print('Input:', example_input)
    print('Expected Output:', ['ac','ca'])
    print('  Actual Output:', get_permutations(example_input))
    
    example_input = 'aca'
    print('Input:', example_input)
    print('Expected Output:', ['aac', 'aca', 'caa'])
    print('  Actual Output:', get_permutations(example_input))