# def calc_discount_factor(r, fr, discount_factor):

#     discount_factor = hyperparameters['discount_factor']
    
#     current_step = r['steps']
#     remaining_steps = fr[(fr['steps'] >= current_step)]

#     agg_discount_factors_sum = sum([ discount_factor ** i * r for i ,r  in enumerate(remaining_steps['reward'].values)])
#     return agg_discount_factors_sum
    

# def get_discounted_reward_for_step(gr):
#     gr['discounted_reward'] = gr.apply(lambda r: calc_discount_factor(r[feature_interests], gr[feature_interests]),axis=1)
#     return gr



