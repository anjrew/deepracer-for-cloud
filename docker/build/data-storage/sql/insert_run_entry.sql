INSERT INTO hyperparameters 
            (
                batch_size, 
                beta_entropy,
                discount_factor, 
                e_greedy_value, 
                epsilon_steps, 
                exploration_type, 
                loss_type, 
                lr, 
                num_episodes_between_training, 
                num_epochs, 
                stack_size, 
                term_cond_avg_score, 
                term_cond_max_episodes, 
                sac_alpha
            )
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
            RETURNING id as hyperparameters_id;

INSERT INTO machine 
            (
                
            )
            VALUES 
            () ON CONFLICT DO NOTHING
            RETURNING id as hyperparameters_id;