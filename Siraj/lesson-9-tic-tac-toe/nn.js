//neural network code
//3 layer feed forward network
//mcb180x <- free course by harvard about the brain
// connects the brain to NN

//convnet.js library also works

var Neural = function (Neural) {
    //this helps with concurrency and deadlocks
    'use strict';

    function getSizes(nodes) {
        return nodes.map(function (layer) {
            return layer.length;
        });
    }

    function makeNode(layerIndex, index, sizes, nodes) {
        //initialize it
        var node = {
            input: 0
        }

        //define cutoff threshold for activation
        if (layerIndex < sizes.length - 1) {
            node.threshold = (typeof nodes === 'undefined') ? 1 : nodes[layerIndex][index].threshold
        }

        //if the node is empty or there is an array with some value in it, return the weight and update the connection in that node
        //define weights
        node.weights = [typeof nodes === 'undefined' ? new Array[sizes[layerIndex + 1]]]: nodes[layerIndex][index].weights.map(function (w) {
            return w;
        });

        return node;
    }

    function Net(sizesOrNodes) {
        var sizes, nodes
        if (Array.isArray(sizesOrNodes) && Array.isArray(sizesOrNodes[0])) {
            sizes = getSizes(sizesOrNodes)
            nodes = sizesOrNodes;
        } else {
            sizes = sizesOrNodes;
        }

        this.nodes = sizes.map(function (size, i) {
            var layer = new Array(size);
            //count num of nodes
            for (var j = 0; j < size; j++) {
                layer[j] = makeNode(i, j, sizes, nodes);
            }
            return layer;
        })
    }

    //weights is a 2d matrix
    Net.prototype.setWeights = function Net_setWeights(weights) {
        //update them via genetic algorithm

        this.eachNode(false, function (node, layerIndex, index) {
            node.weights = weights[layerIndex][index].map(function (w) {
                return w;
            })
        })
    }

    Neural.Net Net;

    return Neural;
}
