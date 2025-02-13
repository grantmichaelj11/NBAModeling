import torch

class MovingAverageModel(torch.nn.Module):
    def __init__(self):
        super().__init__()

        self.input_layer = torch.nn.Linear(6, 128)

        self.hidden_layer1 = torch.nn.Linear(128, 128)
        self.hidden_layer2 = torch.nn.Linear(128, 128)
        self.hidden_layer3 = torch.nn.Linear(128, 128)

        self.output_layer = torch.nn.Linear(128, 1)

        self.activation = torch.nn.LeakyReLU()
    # Initialize Dropout layer outside of forward method
        self.dropout = torch.nn.Dropout(p=0.2)
        
    def forward(self, x):
        x = self.input_layer(x)
        x = self.activation(self.hidden_layer1(x))

        # Apply dropout only during training
        if self.training:
            x = self.dropout(x)
            
        x = self.activation(self.hidden_layer2(x))

        # Apply dropout only during training
        if self.training:
            x = self.dropout(x)

        x = self.activation(self.hidden_layer3(x))

        # Apply dropout only during training
        if self.training:
            x = self.dropout(x)

        x = self.output_layer(x)

        return x