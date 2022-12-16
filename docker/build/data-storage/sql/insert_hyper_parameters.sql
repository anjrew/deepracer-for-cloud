-- MOCK DATA


-- ** WORKS ***
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
            (64, 0.01, 0.99, 0.05, 10000, 'categorical', 'huber', 0.0003, 18, 10, 1, 10000.0, 10000, 0.2)
            RETURNING id as hyperparameters_id;

-- MOCK

-- ** WORKING **
SELECT id FROM hyperparameters 
            WHERE 
                batch_size = 64 AND 
                beta_entropy = 0.01 AND 
                discount_factor = 0.99 AND 
                e_greedy_value = 0.05 AND 
                epsilon_steps = 10000 AND 
                exploration_type = 'categorical' AND 
                loss_type = 'huber' AND 
                lr = 0.0003 AND 
                num_episodes_between_training = 18 AND 
                num_epochs = 10 AND 
                stack_size = 1 AND 
                term_cond_avg_score = 10000.0 AND 
                term_cond_max_episodes = 10000 AND 
                sac_alpha = 0.2;
                

                
-- {
--   "batch_size": 64,
--   "beta_entropy": 0.01,
--   "discount_factor": 0.99,
--   "e_greedy_value": 0.05,
--   "epsilon_steps": 10000,
--   "exploration_type": "categorical",
--   "loss_type": "huber",
--   "lr": 0.0003,
--   "num_episodes_between_training": 18,
--   "num_epochs": 10,
--   "stack_size": 1,
--   "term_cond_avg_score": 10000.0,
--   "term_cond_max_episodes": 10000,
--   "sac_alpha": 0.2
-- }


IF EXISTS (
            SELECT id FROM hyperparameters 
            WHERE 
                batch_size = %s AND 
                beta_entropy = %s AND 
                discount_factor = %s AND 
                e_greedy_value = %s AND 
                epsilon_steps = %s AND 
                exploration_type = %s AND 
                loss_type = %s AND 
                lr = %s AND 
                num_episodes_between_training = %s AND 
                num_epochs = %s AND 
                stack_size = %s AND 
                term_cond_avg_score = %s AND 
                term_cond_max_episodes = %s AND 
                sac_alpha = %s
                RETURNING id as hyperparameters_id;
        ) 
    ELSE
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
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id as hyperparameters_id;
END IF

INsert into runTable

hyperparameters_id


-- DO THIS

WITH s AS (
    SELECT id
    FROM tag
    WHERE key = 'key1' AND value = 'value1'
), i AS (
    INSERT INTO tag ("key", "value")
    SELECT 'key1', 'value1'
    WHERE NOT EXISTS (SELECT 1 FROM s)
    RETURNING id, "key", "value"
)
SELECT id, "key", "value"
FROM i
UNION ALL
SELECT id, "key", "value"
FROM s


-- SECOND 1
-- WITH i AS (
--     INSERT INTO t(a) VALUES ('a') ON CONFLICT (a) DO NOTHING RETURNING id
-- )
-- SELECT id FROM i
-- UNION ALL
-- SELECT id FROM t where a = 'a'
-- limit 1