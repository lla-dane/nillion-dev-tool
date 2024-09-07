This repository essentially contains 2 tools:
1. A library template for achieving random shuffling, such that no number which has been returned before will be returned again
2. A dockerfile for developers, so that they can have nillion-devnet running, without having to worry about all the dependencies

## USAGE
For docs on usage, please refer [usage](./docs/usage.md)


## Motivation

The biggest motivation for implementing the random shuffling library is that it allows developers to build games like blackjack, poker etc by using this library, and acheiving random blind shuffling in their games

For the dockerfile, in case the developer finds themself in need of deploying nillion-devnet, they can use this to deploy, or use this to quickly do the setup, without having to locally do all the steps again and again.
