def calculate_cost(input_tokens, output_tokens, input_price, output_price):

    input_cost = input_tokens / 1000 * input_price

    output_cost = output_tokens / 1000 * output_price

    return input_cost + output_cost
