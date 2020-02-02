let solutions = {};
function poly(a, b, c) {
    $.ajax({
        method: "POST",
        url: "/calculator/solve",
        data: JSON.stringify({coeffs: [a, b, c]}),
        success: function (result) {
            solutions = result;
            let solution_div = document.getElementById("solution");
            solution_div.innerHTML = "";
            Object.keys(solutions).forEach(function (solution_name){
               let solution_table = solve(solution_name, solutions[solution_name]);
               solution_div.appendChild(solution_table);
            });
            // console.log(result);
            // solve(result);
        }
    });
}

function solve(solution_name, solution) {
    // let solution = result["delta"];
    let solution_table = document.createElement("table");
    solution["steps"].forEach(function (step) {
        if ("pre" in step) {
            let step_pre_tr = document.createElement('tr');
            let step_pre_td0 = document.createElement("td");
            let step_pre_td = document.createElement("td");
            step_pre_td.innerHTML = step["pre"];
            step_pre_tr.appendChild(step_pre_td0);
            step_pre_tr.appendChild(step_pre_td);
            solution_table.appendChild(step_pre_tr);
        }
        let step_formula_td = document.createElement("td");
        let formula_step = false;
        if ("formula" in step) {
            step["formula"].forEach(function (formula) {
                formula_step = true;
                let step_formula_tr = document.createElement('tr');
                let step_formula_td0 = document.createElement("td");
                step_formula_td0.innerHTML = formula;
                step_formula_tr.appendChild(step_formula_td0);
                step_formula_tr.appendChild(step_formula_td);
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, step_formula_td0]);
                solution_table.appendChild(step_formula_tr);
            });
            // step_div.appendChild(step_formula);
        }
        if ("parr" in step){
            step["parr"].forEach(function (parr) {
                let step_parr_tr = document.createElement('tr');
                let step_parr_td0 = document.createElement("td");
                let step_parr_td = document.createElement("td");
                step_parr_td0.innerHTML = parr[0];
                step_parr_td.innerHTML = parr[1];
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, step_parr_td0]);
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, step_parr_td]);
                step_parr_tr.appendChild(step_parr_td0);
                step_parr_tr.appendChild(step_parr_td);
                solution_table.appendChild(step_parr_tr);

            })
        }
        if ("post" in step) {
            if (formula_step){
               step_formula_td.innerHTML = step["post"];
            }else{
                let step_post_tr = document.createElement('tr');
                let step_post_td = document.createElement("td");
                let step_post_td0 = document.createElement("td");
                step_post_tr.appendChild(step_post_td0);
                step_post_td.innerHTML = step["post"];
                step_post_tr.appendChild(step_post_td);
                solution_table.appendChild(step_post_tr);
            }
        }
    })
    return solution_table
}