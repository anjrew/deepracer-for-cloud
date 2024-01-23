# Explanation of Hyperparameters

"batch_size": TODO,
"beta_entropy": TODO,
"discount_factor": HOW future rewards are discounted,


## e_greedy_value
  
The probability of choosing a random action instead of the best action.
This value is linearly annealed from 1.0 to 0.1 over epsilon_steps.
This value is only used if exploration_type is "e_greedy".
So if this value is set to 1 then the agent will always choose a random action.
If this value is set to 0 then the agent will always choose the best action.
If the value is set to 0.1 then the agent will choose a random action 10% of the time.

```python
    def select_action(self, state):
        # Select the action with the highest Q(s,a) with probability 1 - epsilon (exploitation)
        if np.random.rand() >= self.epsilon:
            return np.argmax(self.q[state])
        # Select a random action with probability epsilon (exploration)
        else:
            return np.random.randint(len(self.q[state]))
```

## beta_entropy

Purpose: It is a coefficient that scales the entropy bonus in the loss function. Entropy in the context of RL is a measure of randomness or unpredictability in the policy's action distribution.
Role in PPO: By adding an entropy bonus (scaled by beta_entropy) to the loss function, the algorithm encourages exploration. A higher entropy means the policy is more random, which can be beneficial for exploring the environment thoroughly.
Impact: Adjusting beta_entropy affects the balance between exploration (trying new actions) and exploitation (using known rewarding actions). A higher value promotes exploration, while a lower value leans towards exploitation.


Choosing between **beta_entropy** and **e_greedy_value** in Proximal Policy Optimization (PPO) depends on the specific requirements of your reinforcement learning environment and the behavior you want from your agent. Here's a guide to help you decide:

- Using Beta Entropy (beta_entropy):
      Complex or Continuous Action Spaces: beta_entropy is particularly useful in environments with complex or continuous action spaces, where promoting a diverse range of actions helps in exploring the space more effectively.
      Preventing Premature Convergence: If your agent is converging too quickly to suboptimal policies, increasing beta_entropy can encourage more exploration, potentially leading to better solutions.
      Fine-Tuning Exploration: beta_entropy offers a more nuanced control over the agent's exploration behavior, as it affects the stochasticity of the policy itself.

- Using Epsilon Greedy Value (e_greedy_value):
      Discrete Action Spaces: In environments with discrete action spaces, an ε-greedy strategy (controlled by e_greedy_value) can be a straightforward and effective way to balance exploration and exploitation.
      Simple or Well-Understood Environments: In cases where the environment is relatively simple or well-understood, ε-greedy can be an easy-to-implement method that provides sufficient exploration.
      Early Stages of Learning: In the initial stages of training, a higher e_greedy_value can be used to encourage broad exploration, which can then be gradually decreased as the agent starts learning effective strategies.
      
  <!-- "epsilon_steps": 10000,
  "exploration_type": "categorical",
  "loss_type": "huber",
  "lr": 0.00001,
  "num_episodes_between_training": 15,
  "num_epochs": 10,
  "stack_size": 1,
  "term_cond_avg_score": 10000.0,
  "term_cond_max_episodes": 10000,
  "sac_alpha": 0.2 -->
}