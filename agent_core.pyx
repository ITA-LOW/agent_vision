# agent_core.pyx

def context_matches(dict context, dict beliefs):
    """
    Verifica se todos os pares (chave, valor) de context existem e são iguais em beliefs.
    """
    cdef object key, value
    for key, value in context.items():
        # Usar beliefs.get(key) evita duas buscas separadas; se o valor não bater, retorna False.
        if beliefs.get(key) != value:
            return False
    return True

def get_plan_for_goal(list plan_list, dict beliefs):
    """
    Itera sobre uma lista de planos e retorna o primeiro cuja chave 'context'
    seja compatível com as crenças.
    """
    cdef int i
    for i in range(len(plan_list)):
        plan_entry = plan_list[i]
        if context_matches(plan_entry['context'], beliefs):
            return plan_entry['plan']
    return None
