def next_permutation(nums):
    # Find the first element from the right that is smaller than its next element
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    # If no such element is found, it means the given permutation is the highest
    if i == -1:
        return None
    # Find the smallest element to the right of 'i' that is greater than nums[i]
    j = len(nums) - 1
    while nums[j] <= nums[i]: 
        j -= 1
    # Swap nums[i] and nums[j]
    nums[i], nums[j] = nums[j], nums[i]
    # Reverse the subarray to the right of 'i'
    nums[i + 1:] = reversed(nums[i + 1:])
    return nums

def find_next_permutation(number):
    # Convert the number to a list of digits
    nums = [int(digit) for digit in str(number)]
    # Find the next permutation
    next_perm = next_permutation(nums)
    # If the given permutation is already the highest, return None
    if next_perm is None:
        return None
    # Convert the list of digits back to an integer
    result = int(''.join(map(str, next_perm)))
    return result

def main():
    try:
        user_input = None
        while True:
            if user_input is None:
                user_input = int(input("Enter a number: "))
            else:
                print("Using result from previous iteration:", user_input)
            result = find_next_permutation(user_input)
            if result is not None:
                print("Next permutation:", result)
            else:
                print("The given permutation is already the highest.")         
            # Ask the user if they want to continue
            action = input("Press ';' to continue with the result, or any other key to exit: ")
            if action != ';':
                break
            else:
                user_input = result
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
