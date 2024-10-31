import typing

EmptyTokens2D = typing.TypedDict('EmptyTokens2D', {'empty': int})
EmptyTokens: EmptyTokens2D = {
    'empty': 2
}

SecretBlocks2D = typing.TypedDict('SecretBlocks2D', {'full': int, 'empty': int})
SecretBlocks: SecretBlocks2D = {
    'full': 3,
    'empty': 4
}

BreakableBlocks2D = typing.TypedDict('BreakableBlocks2D', {'breakable': int})
BreakableBlocks: BreakableBlocks2D = {
    'breakable': 1
}

GroundTokens2D = typing.TypedDict('GroundTokens2D', {'ground': int})
GroundTokens: GroundTokens2D = {
    'ground': 0,
}

EnemiesTokens2D = typing.TypedDict('EnemiesTokens2D', {'goomba': int})
EnemiesTokens = {
    'goomba': 5,
}