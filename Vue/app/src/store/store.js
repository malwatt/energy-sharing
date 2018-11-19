import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const model_parameters = {
    state: {

    },

    mutations: {
        save_server_page(state, payload) {
            state[payload.model_page_name] = payload.data;
            console.log(state);
        }
    }
};

const frontend_state = {
    state: {

    },

    getters: {

    },

    mutations: {
        save_page(state, payload) {
            state[payload.model_page_name] = payload.data;
        }
    }
};

export const store = new Vuex.Store({
    strict: true,
    modules: {
        model_parameters: model_parameters,
        frontend_state: frontend_state,
    },

    state: {

    },

    getters: {

    },
    mutations: {
        setValue (state, payload) {
            state.output_data[payload.input_page][payload.field_name] = payload.value
        },

        setTableDropdown (state, payload) {
            state.output_data[payload.input_page][payload.array_name][payload.row_index][payload.field_name] = payload.value
        },

        addRow(state, payload) {
            state.output_data[payload.input_page][payload.field_name].push(payload.row)
        },
    },
});


